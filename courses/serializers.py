from rest_framework import serializers
from .models import Course, Enrollment
from students.models import Student


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class EnrollmentGetSerializer(serializers.ModelSerializer):
    course_of_study = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = "__all__"


class EnrollmentStudentGetSerializer(serializers.ModelSerializer):
    course_of_study = CourseSerializer()

    class Meta:
        model = Enrollment
        exclude = ["student"]


class EnrollmentPostSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    street_address = serializers.CharField(max_length=200)
    city = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=256)
    phone_number = serializers.CharField(max_length=20)
    gender = serializers.ChoiceField(choices=Enrollment.GENDERS)
    date_of_birth = serializers.DateField()
    image = serializers.ImageField(required=False)

    guardian_first_name = serializers.CharField(max_length=50)
    guardian_last_name = serializers.CharField(max_length=50)
    guardian_phone_number = serializers.CharField(max_length=20)
    guardian_email = serializers.EmailField(max_length=256)
    guardian_relationship = serializers.CharField(max_length=50)
    guardian_address = serializers.CharField(max_length=256)

    highest_qualification = serializers.CharField(max_length=50)
    school_attended = serializers.CharField(max_length=50, required=False)

    course_of_study = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    session = serializers.ChoiceField(choices=Enrollment.SESSIONS)
    learning_center = serializers.ChoiceField(choices=Enrollment.LEARNING_CENTERS)

    def create(self, validated_data):
        student = Student.objects.get(user=self.context["request"].user)
        course_of_study = validated_data["course_of_study"]
        try:
            enrollment = Enrollment.objects.get(student=student, course_of_study=course_of_study)
            if not enrollment.paid:
                raise serializers.ValidationError("You are already enrolled in this course. But you have not paid.")
            raise serializers.ValidationError("You are already enrolled in this course.")
        except Enrollment.DoesNotExist:
            enrollment = Enrollment.objects.create(
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                street_address=validated_data["street_address"],
                city=validated_data["city"],
                state=validated_data["state"],
                country=validated_data["country"],
                email=validated_data["email"],
                phone_number=validated_data["phone_number"],
                gender=validated_data["gender"],
                date_of_birth=validated_data["date_of_birth"],
                guardian_first_name=validated_data["guardian_first_name"],
                guardian_last_name=validated_data["guardian_last_name"],
                guardian_phone_number=validated_data["guardian_phone_number"],
                guardian_email=validated_data["guardian_email"],
                guardian_relationship=validated_data["guardian_relationship"],
                guardian_address=validated_data["guardian_address"],
                highest_qualification=validated_data["highest_qualification"],
                school_attended=validated_data["school_attended"],
                course_of_study=course_of_study,
                session=validated_data["session"],
                learning_center=validated_data["learning_center"],
                student=student,
                paid=False,
                scholarship=False,
            )
            enrollment.save()

            return self.validated_data
