# define signals callback
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FilmComments, PersonSummary, GradeSummary 

@receiver(post_save, sender=FilmComments, dispatch_uid="count_grade")
def django_trigger(sender, **kwargs):
    # get the insert data instance
    s_ins = kwargs['instance']  
    # update personsummary table
    try:
        ps = PersonSummary.objects.get(cus_name=s_ins.cus_name)
    except PersonSummary.DoesNotExist as e:
        ps = PersonSummary(cus_name=s_ins.cus_name)
    finally:
        if(s_ins.grade == '力荐'):
            ps.high_recommend += 1
        elif(s_ins.grade == '推荐'):
            ps.recommend += 1
        elif(s_ins.grade == '还行'):
            ps.general += 1
        elif(s_ins.grade == '较差'):
            ps.poor += 1
        elif(s_ins.grade == '很差'):
            ps.very_poor += 1
        ps.sum += 1
        ps.save()   

    # update gradesummary table
    try:
        ps = GradeSummary.objects.get(film_name=s_ins.film_name)
    except GradeSummary.DoesNotExist as e:
        ps = GradeSummary(film_name=s_ins.film_name)
    finally:
        if(s_ins.grade == '力荐'):
            ps.high_recommend += 1
        elif(s_ins.grade == '推荐'):
            ps.recommend += 1
        elif(s_ins.grade == '还行'):
            ps.general += 1
        elif(s_ins.grade == '较差'):
            ps.poor += 1
        elif(s_ins.grade == '很差'):
            ps.very_poor += 1
        ps.sum += 1    
        ps.save()    
