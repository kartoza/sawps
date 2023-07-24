import base64

from django.contrib.auth.models import User
from django.db.models import Sum
from django.test import Client, TestCase
from django.urls import reverse
from frontend.utils.organisation import CURRENT_ORGANISATION_ID_KEY
from population_data.models import AnnualPopulation
from property.factories import PropertyFactory
from rest_framework import status
from species.factories import OwnedSpeciesFactory, TaxonFactory, TaxonRankFactory
from species.models import TaxonRank
from stakeholder.factories import organisationFactory, organisationUserFactory


class SpeciesPopuationCountTestCase(TestCase):
    def setUp(self):
        taxon_rank = TaxonRank.objects.filter(name="Species").first()
        if not taxon_rank:
            taxon_rank = TaxonRankFactory.create(name="Species")

        self.taxon = TaxonFactory.create(
            taxon_rank=taxon_rank, common_name_varbatim="Lion"
        )

        user = User.objects.create_user(username="testuserd", password="testpasswordd")

        self.organisation_1 = organisationFactory.create()
        organisationUserFactory.create(user=user, organisation=self.organisation_1)

        self.property = PropertyFactory.create(
            organisation=self.organisation_1, name="PropertyA"
        )

        self.owned_species = OwnedSpeciesFactory.create_batch(
            5, taxon=self.taxon, user=user, property=self.property
        )

        self.url = reverse(
            "species_population_count",
            kwargs={"property_id": self.property.id},
        )

        self.auth_headers = {
            "HTTP_AUTHORIZATION": "Basic "
            + base64.b64encode(b"testuserd:testpasswordd").decode("ascii"),
        }
        self.client = Client()

        session = self.client.session
        session[CURRENT_ORGANISATION_ID_KEY] = self.organisation_1.id
        session.save()

    def test_species_population_count(self):
        owned_species = OwnedSpeciesFactory(taxon__common_name_varbatim="Lion")
        url = self.url
        data = {"species": "Lion"}
        response = self.client.get(url, data, **self.auth_headers)
        annual_populations = (
            AnnualPopulation.objects.filter(owned_species=owned_species)
            .values("month")
            .annotate(month_total=Sum("total"))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["annualpopulation_count"][0].get("month_total"),
            annual_populations[0].get("month_total"),
        )
