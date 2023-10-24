from rest_framework import serializers

# import model from models.py
from bleeding.models import *
from fabry.models import *
from glycogen.models import *
from iem.models import *
from mucopoly.models import *
from nmd.models import *
from pid.models import *
from pompe.models import *
from skeletal.models import *
from smallmolecule.models import *
from storage.models import *
from thalasemia.models import *
from .models import *

# Create a model serializer
class GeeksSerializer(serializers.ModelSerializer):
    # specify model and fields
    class Meta:
        model = profile_bleeding
        fields = '__all__'