# from django.db import model
from django.conf import settings
from django.db import models as defaultModel
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.contrib.auth.models import User, Group
from drawing.models import AOI as drawing_AOI
from features.registry import register
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django import forms
from ckeditor.fields import RichTextField

# Create your models here.
@register
class AOI(drawing_AOI):

	class Options:
		verbose_name = 'Area of Interest'
		icon_url = 'hnfp/img/aoi.png'
		export_png = False
		manipulators = []
		# optional_manipulators = ['clipping.manipulators.ClipToShoreManipulator']
		optional_manipulators = []
		form = 'drawing.forms.AOIForm'
		# form_template = 'aoi/form.html'
		form_template = 'hnfp/aoi/form.html'
		show_template = 'aoi/show.html'

class ShareObservationWithManager(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	share = models.BooleanField(
		default=False,
	)

	def user_is_sharing(userpk):
		sharing = ShareObservationWithManager.objects.get(user=userpk)
		return sharing

# blog posts for forum
class PublicManager(models.Manager):
	def get_queryset(self):
		return super(PublicManager, self).get_queryset()\
										 .filter(publish__lte=timezone.now())

class Post(models.Model):
	STATUS_CHOICES = (
		('Draft', 'draft'),
		('Published', 'published'),
	)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	body = models.TextField()
	allow_comments = models.BooleanField('allow comments', default=True)
	is_event = models.BooleanField('event', default=False)
	publish = models.DateTimeField(default=timezone.now)
	objects = PublicManager()  # Our custom manager.

	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail',
					   kwargs={'year': self.publish.year,
							   'month': self.publish.strftime('%b'),
							   'day': self.publish.strftime('%d'),
							   'slug': self.slug})

# registration survey
class SurveyResults(models.Model):

	forest_use_hunt_deer = models.CharField(
		max_length=4000,
		blank=True,
		null=True,
	)
	forest_use_gather_herbs = models.CharField(
		max_length=4000,
		blank=True,
		null=True,
	)
	forest_use_fish = models.CharField(
		max_length=4000,
		blank=True,
		null=True,
	)
	forest_use_collect_berries = models.CharField(
		max_length=4000,
		blank=True,
		null=True,
	)
	forest_use_gather_mushrooms = models.CharField(
		max_length=4000,
		blank=True,
		null=True,
	)
	forest_use_collect_firewood = models.CharField(
		max_length=4000,
		blank=True,
		null=True,
	)
	forest_use_other_activities = models.CharField(
		max_length=4000,
		blank=True,
		null=True,
	)

	forest_use_other = models.CharField(
		max_length=4000,
		blank=True,
		null=True,
	)

	rank_hunt = models.CharField(
		max_length=400,
		blank=True,
		null=True,
	)
	rank_gather_herbs = models.CharField(
		max_length=400,
		blank=True,
		null=True,
	)
	rank_fish = models.CharField(
		max_length=400,
		blank=True,
		null=True,
	)
	rank_collect_berries = models.CharField(
		max_length=400,
		blank=True,
		null=True,
	)
	rank_gather_mushrooms = models.CharField(
		max_length=400,
		blank=True,
		null=True,
	)
	rank_collect_firewood = models.CharField(
		max_length=400,
		blank=True,
		null=True,
	)
	rank_other = models.CharField(
		max_length=4000,
		blank=True,
		null=True,
	)

	gender = models.CharField(
		max_length=400,
		blank=True,
		null=True,
	)

	employment_forest_dependent = models.CharField(
		max_length=400,
		blank=True,
		null=True,
	)

	occupation = models.CharField(
		max_length=400,
		blank=True,
		null=True
	)

	regiontally = models.CharField(
		max_length=4000,
		blank=True,
		null=True,
	)

	class Meta:
		verbose_name_plural = 'Survey Responses'

	def __unicode__(self):
		return (self.id)

	def get_survey_results():
		return SurveyResults.objects.all()

class Survey(models.Model):
	name = models.CharField(max_length=400)
	description = models.TextField()

	def __unicode__(self):
		return (self.name)

	def questions(self):
		if self.pk:
			return Question.objects.filter(survey=self.pk)
		else:
			return None

class Category(models.Model):
	name = models.CharField(max_length=400)
	survey = models.ForeignKey(Survey)

	def __unicode__(self):
		return (self.name)

def validate_list(value):
	'''takes a text value and verifies that there is at least one comma '''
	values = value.split(',')
	if len(values) < 2:
		raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")

class Question(models.Model):
	TEXT = 'Text'
	RADIO = 'Radio'
	SELECT = 'Select'
	SELECT_MULTIPLE = 'Select Multiple'
	INTEGER = 'Integer'

	QUESTION_TYPES = (
		(TEXT, 'text'),
		(RADIO, 'radio'),
		(SELECT, 'select'),
		(SELECT_MULTIPLE, 'select_multiple'),
		(INTEGER, 'integer'),
	)

	text = models.TextField()
	required = models.BooleanField()
	category = models.ForeignKey(Category, blank=True, null=True,)
	survey = models.ForeignKey(Survey)
	question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
	# the choices field is only used if the question type
	choices = models.TextField(blank=True, null=True,
		help_text='if the question type is "radio," "select," or "select multiple" provide a comma-separated list of options for this question .')

	def save(self, *args, **kwargs):
		if (self.question_type == Question.RADIO or self.question_type == Question.SELECT
			or self.question_type == Question.SELECT_MULTIPLE):
			validate_list(self.choices)
		super(Question, self).save(*args, **kwargs)

	def get_choices(self):
		''' parse the choices field and return a tuple formatted appropriately
		for the 'choices' argument of a form widget.'''
		choices = self.choices.split(',')
		choices_list = []
		for c in choices:
			c = c.strip()
			choices_list.append((c,c))
		choices_tuple = tuple(choices_list)
		return choices_tuple

	def __unicode__(self):
		return (self.text)

class Response(models.Model):
	# a response object is just a collection of questions and answers with a
	# unique interview uuid
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	survey = models.ForeignKey(Survey)
	interviewer = models.CharField('Name of Interviewer', max_length=400)
	interviewee = models.CharField('Name of Interviewee', max_length=400)
	conditions = models.TextField('Conditions during interview', blank=True, null=True)
	comments = models.TextField('Any additional Comments', blank=True, null=True)
	interview_uuid = models.CharField("Interview unique identifier", max_length=36)

	def __unicode__(self):
		return ("response %s" % self.interview_uuid)

class AnswerBase(models.Model):
	question = models.ForeignKey(Question)
	response = models.ForeignKey(Response)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

# these type-specific answer models use a text field to allow for flexible
# field sizes depending on the actual question this answer corresponds to. any
# "required" attribute will be enforced by the form.
class AnswerText(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerRadio(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerSelect(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerSelectMultiple(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerInteger(AnswerBase):
	body = models.IntegerField(blank=True, null=True)

# Job Postings
class JobOpportunity(models.Model):
	title = models.CharField(max_length=400)
	posted = models.DateTimeField(auto_now_add=True)
	description = RichTextField(blank=True, null=True, config_name="custom") #ckeditor
	is_html = models.BooleanField(default=False, help_text='Use HTML editor')
	html_content = models.TextField(blank=True, null=True, help_text='html if use html == True')
	jop_post_doc = models.FileField(blank=True, upload_to='job-post/')

	class Meta:
		verbose_name_plural = 'Job Opportunities'

	def __unicode__(self):
		return unicode("%s" % (self.page))

	def __str__(self):
		return self.title

# observations
class Observation(models.Model):
	OBSERVATION_CATS = (
		('Bear', 'bear'),
		('Deer', 'deer'),
		('Medicinal Herbs', 'medicinal_herbs'),
		('Shrimp', 'shrimp'),
		('Berries', 'berries'),
		('Firewood', 'firewood'),
		('Mushrooms', 'mushrooms'),
		('Crab', 'crab'),
		('Shellfish', 'shellfish'),
		('Salmon', 'salmon'),
		('Other Fish', 'other_fish'),
		('Basket Making', 'basket_making'),
		('Custom', 'custom'),
	)

	category = models.CharField(
		max_length=400,
		choices=OBSERVATION_CATS,
		default='custom'
	)
	customcategory = models.CharField(
		max_length=400,
		null=True,
		blank=True,
	)
	observation_date = models.CharField(
		max_length=100,
		null=True,
		blank=True
	)
	observation_time = models.CharField(
		max_length=20,
		blank=True,
		null=True
	)
	observation_type = models.CharField(
		max_length=400,
		blank=True,
		null=True
	)
	observation_tally = models.CharField(
		max_length=100,
		default=1,
		blank=True,
		null=True,
	)
	observation_created = models.DateTimeField(
		auto_now_add=True
	)
	observation_updated = models.DateTimeField(
		auto_now=True
	)
	number_of_observers = models.CharField(
		max_length=100,
		default=1,
		null=True,
		blank=True,
	)

	observation_photo = models.ImageField(
		upload_to='observations/%Y/%m/%d',
		max_length=2000,
		null=True,
		blank=True,
	)

	observer_username = models.CharField(
		max_length=800,
		null=True,
		blank=True,
	)

	observation_location = models.PointField(
		srid=settings.GEOMETRY_DB_SRID,
		default=None,
		null=True,
		blank=True,
	)
	comments = models.CharField(
		max_length=20000,
		default=None,
		null=True,
		blank=True,
	)

	def to_dict(self):
		if self.observation_location is not None:
			point = self.observation_location.geojson
		else:
			point = None
		if self.observation_photo:
			photo = self.observation_photo.url
		else:
			photo = ''
		return {
			'category': self.category,
			'customcategory': self.customcategory,
			'observation_date': self.observation_date,
			'observation_time': self.observation_time,
			'observation_type': self.observation_type,
			'observation_tally': self.observation_tally,
			'number_of_observers': self.number_of_observers,
			'observer_username': self.observer_username,
			'observation_location': point,
			'observation_photo': photo,
			'comments': self.comments,
			'id': self.id,
		}

	def __str__(self):
		return "{}: `{}`".format(self.observation_location, self.category)

	class Meta:
		verbose_name_plural = 'Observations'

	def get_categories():
		cats = Observation.OBSERVATION_CATS
		cats_list = []
		for cat in cats:
			cats_list.append(cat[0])
		return cats_list

	def get_user_observations(username):
		return Observation.objects.filter(observer_username=username)

	def get_absolute_url(self):
		return reverse('observation_detail', kwargs={'pk': self.pk})

# alerts
class Alert(models.Model):
	alert_date = models.CharField(
		max_length=100,
		null=True,
		blank=True
	)
	alert_time = models.CharField(
		max_length=20,
		blank=True,
		null=True
	)
	alert_type = models.CharField(
		max_length=400,
		blank=True,
		null=True
	)
	alert_created = models.DateTimeField(
		auto_now_add=True
	)
	alert_updated = models.DateTimeField(
		auto_now=True
	)
	alert_username = models.CharField(
		max_length=800,
		null=True,
		blank=True,
	)
	alert_location = models.PointField(
		srid=settings.GEOMETRY_DB_SRID,
		default=None,
		null=True,
		blank=True,
	)
	alert_comment = models.CharField(
		max_length=20000,
		default=None,
		null=True,
		blank=True,
	)
	alert_confirmed = models.BooleanField(
		default=False
	)

	alert_photo = models.ImageField(
		upload_to='alerts/%Y/%m/%d',
		max_length=2000,
		null=True,
		blank=True,
	)

	def to_dict(self):
		if self.alert_location is not None:
			point = self.alert_location.geojson
		else:
			point = None

		if self.alert_photo:
			photo = self.alert_photo.url
		else:
			photo = ''

		return {
			'alert_date': self.alert_date,
			'alert_time': self.alert_time,
			'alert_type': self.alert_type,
			'alert_username': self.alert_username,
			'alert_location': point,
			'alert_comment': self.alert_comment,
			'alert_photo': photo,
			'alert_id': self.id,
		}

	def __str__(self):
		return "{}: `{}`".format(self.alert_location, self.alert_type)

	class Meta:
		verbose_name_plural = 'Alerts'

	def get_user_alerts(username):
		return Alert.objects.filter(alert_username=username)

	def get_absolute_url(self):
		return reverse('alert_detail', kwargs={'pk': self.pk})

# Ecosystems services table
class Resource(models.Model):
	name = models.CharField(
		max_length=4000,
		default='Resource Name',
	)
	def get_resources():
		return Resource.objects.all()

# type of impact such as increase or decrease
class ImpactType(models.Model):
	name = models.CharField(
		max_length=4000,
		default='Impact Type',
	)
	def get_impact_types():
		return ImpactType.objects.all()

class ProjectResourceImpact(models.Model):
	# project =
	resource = models.ForeignKey(Resource, default=1)
	impactType = models.ForeignKey(ImpactType, default=1)

# Land use projects
class LandUseProject(models.Model):
	ECOSYSTEM_IMPACTS = (
		('Increase', 'increase'),
		('Decrease', 'decrease'),
		('No Change', 'no_change'),
	)
	ECOSYSTEM_SERVICE = (
		('Deer', 'deer'),
		('Berries', 'berries'),
		('Raw materials', 'materials'),
		('Fresh water', 'water'),
		('Medicinal herbs', 'medicinal'),
		('Carbon sequestration', 'sequestration'),
		('Soil erosion and fertility', 'soil'),
		('Reduce damage caused by extreme events', 'protection'),
		('Climate and air quality', 'climate'),
		('Pollination', 'pollination'),
		('Water Treatment', 'water_treatment'),
		('Biological Control', 'biological_control'),
		('Habitat for species', 'habitat'),
		('Maintenance of genetic diversity', 'diversity'),
		('Tourism', 'tourism'),
		('Aesthetic appreciation and inspiration for culture', 'culture'),
		('Spiritual experience and identity', 'spiritual'),
		('Recreation', 'recreation')
	)
	name = models.CharField(
		max_length=300,
		null=True,
		blank=True,
	)
	category = models.CharField(
		max_length=400,
		blank=True,
		null=True,
	)
	summary = models.CharField(
		max_length=20000,
		default=None,
		null=True,
		blank=True,
	)
	description = models.CharField(
		max_length=20000,
		default=None,
		null=True,
		blank=True,
	)
	start_date = models.CharField(
		max_length=200,
		null=True,
		blank=True
	)
	completion_date = models.CharField(
		max_length=200,
		null=True,
		blank=True
	)
	actions = models.CharField(
		max_length=20000,
		null=True,
		blank=True,
	)

	# projectResourceImpact = models.ForeignKey('ProjectResourceImpact', default=1)

	dollar_costs = models.CharField(
		max_length=4000,
		null=True,
		blank=True,
	)
	emdollars = models.CharField(
		max_length=4000,
		null=True,
		blank=True,
	)
	area = models.MultiPolygonField(
		srid=settings.GEOMETRY_DB_SRID,
		default=None,
		null=True,
		blank=True,
	)
	created = models.DateTimeField(
		auto_now_add=True
	)
	updated = models.DateTimeField(
		auto_now=True
	)
	published = models.BooleanField(
		default=False
	)
	share_with_land_managers = models.BooleanField(
		default=False
	)
	username = models.CharField(
		max_length=400,
		null=True,
		blank=True,
	)

	def to_dict(self):
		if self.area is not None:
			polygon = self.area.geojson
		else:
			polygon = None
		return {
			'area': polygon,
			'name': self.name,
			'category': self.category,
			'summary': self.summary,
			'description': self.description,
			'username': self.username,
			'start_date': self.start_date,
			'completion_date': self.completion_date,
			'actions': self.actions,
			'dollar_costs': self.dollar_costs,
			'published': self.published,
			'share_with_land_managers': self.share_with_land_managers,
			'id': self.id,
		}

	def __str__(self):
		return "{}: `{}`".format(self.area, self.category)

	class Meta:
		verbose_name_plural = 'Land Use Projects'

	def get_categories():
		cats = LandUseProject.PROJ_CATS
		cats_list = []
		for cat in cats:
			cats_list.append(cat[0])
		return cats_list

	def get_user_proj(username):
		return LandUseProjects.objects.filter(username=username)

	def get_absolute_url(self):
		return reverse('landuse_detail', kwargs={'pk': self.pk})
