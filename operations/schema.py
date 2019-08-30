from django.db.models import Q
from graphene import ObjectType, List, Schema, Int, String, relay, Field, Connection, Node
from graphene_django.filter import DjangoFilterConnectionField

from .models import Baby, VaccineSchedule, VaccineRecord
from graphene_django import DjangoObjectType


class ExtendedConnection(Connection):
	class Meta:
		abstract = True

	total_count = Int()
	edge_count = Int()

	def resolve_total_count(root, info, **kwargs):
		return root.length

	def resolve_edge_count(root, info, **kwargs):
		return len(root.edges)


class BabyGraphModel(DjangoObjectType):
	class Meta:
		model = Baby
		filter_fields = ['first_name', 'last_name', 'week']
		interfaces = (relay.Node,)

		connection_class = ExtendedConnection

	summary = Int()

	def resolve_summary(self, info):
		return Baby.objects.filter(week=self.week).count()


class VaccineScheduleGraphModel(DjangoObjectType):
	class Meta:
		model = VaccineSchedule
		filter_fields = ['week', 'vaccine', 'status', 'baby']
		interfaces = (Node, )
		connection_class = ExtendedConnection


class VaccineRecordGraphModel(DjangoObjectType):
	class Meta:
		model = VaccineRecord
		filter_fields = ['vaccine', 'status']
		interfaces = (Node, )
		connection_class = ExtendedConnection


class Query(ObjectType):
	all_babies = List(BabyGraphModel)
	all_babies_by_week = DjangoFilterConnectionField(BabyGraphModel)
	baby = List(BabyGraphModel, week=Int())

	vaccines = DjangoFilterConnectionField(VaccineScheduleGraphModel)
	vaccine_records = DjangoFilterConnectionField(VaccineRecordGraphModel)

	def resolve_vaccines(self, info, *args, **kwargs):
		week = kwargs.get('week')
		vaccine = kwargs.get('vaccine')
		status = kwargs.get('status')
		baby = kwargs.get('baby')

		if week is not None:
			return VaccineSchedule.objects.filter(week=week)
		if vaccine is not None:
			return VaccineSchedule.objects.filter(vaccine=vaccine)
		if baby is not None:
			return VaccineSchedule.objects.filter(baby=baby)
		if status is not None:
			return VaccineSchedule.objects.filter(status=status)
		return None

	def resolve_vaccine_records(self, info, *args, **kwargs):
		vaccine = kwargs.get('vaccine')
		status = kwargs.get('status')
		baby = kwargs.get('baby')

		if vaccine is not None:
			return VaccineRecord.objects.filter(vaccine=vaccine)
		if baby is not None:
			return VaccineRecord.objects.filter(baby=baby)
		if status is not None:
			return VaccineRecord.objects.filter(status=status)
		return None

	def resolve_all_babies(self, info):
		return Baby.objects.all()

	def resolve_baby(self, info, week):
		return Baby.objects.filter(week=week)


schema = Schema(query=Query)
