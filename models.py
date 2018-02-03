# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FilmComments(models.Model):
    id = models.AutoField(primary_key=True)
    cus_name = models.TextField(db_column='CUS_NAME')  # Field name made lowercase.
    film_name = models.TextField(db_column='FILM_NAME')  # Field name made lowercase.
    comment = models.TextField(db_column='COMMENT')  # Field name made lowercase.
    grade = models.TextField(db_column='GRADE', blank=True, null=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='TIME')  # Field name made lowercase.
    source = models.TextField(db_column='SOURCE')  # Field name made lowercase.

    @classmethod
    def was_filtered_by(self, cname = None, fname = None, gr = None):
        '''
        return a dictionary contains filtered results;
        '''
        c = self.objects
        try:
            if(cname):
                c = c.filter(cus_name = cname)
            if(fname):
                c = c.filter(film_name = fname)
            if(gr):
                c = c.filter(grade = gr)
        except Exception as e:
            print("Error: {}".format(e.args[0]))
        finally:
            return c.order_by('-time').values()
    
    @classmethod
    def is_existed(self, ti):
        try:
            self.objects.get(time=ti)
        except self.DoesNotExist as e:
            return False
        else:
            return True 


    class Meta:
        db_table = 'film_comments'

class GradeSummary(models.Model):
    film_name = models.CharField(db_column='FILM_NAME', max_length=50, primary_key=True)  # Field name made lowercase.
    high_recommend = models.IntegerField(db_column='HIGH_RECOMMEND', default=0)  # Field name made lowercase.
    recommend = models.IntegerField(db_column='RECOMMEND', default=0)  # Field name made lowercase.
    general = models.IntegerField(db_column='GENERAL', default=0)  # Field name made lowercase.
    poor = models.IntegerField(db_column='POOR', default=0)  # Field name made lowercase.
    very_poor = models.IntegerField(db_column='VERY_POOR', default=0)  # Field name made lowercase.
    sum = models.IntegerField(db_column='SUM', default=0)  # Field name made lowercase.

    class Meta:
        db_table = 'grade_summary'


class PersonSummary(models.Model):
    cus_name = models.CharField(db_column='CUS_NAME', max_length=50, primary_key=True)  # Field name made lowercase.
    high_recommend = models.IntegerField(db_column='HIGH_RECOMMEND', default=0)  # Field name made lowercase.
    recommend = models.IntegerField(db_column='RECOMMEND', default=0)  # Field name made lowercase.
    general = models.IntegerField(db_column='GENERAL', default=0)  # Field name made lowercase.
    poor = models.IntegerField(db_column='POOR', default=0)  # Field name made lowercase.
    very_poor = models.IntegerField(db_column='VERY_POOR', default=0)  # Field name made lowercase.
    sum = models.IntegerField(db_column='SUM', default=0)  # Field name made lowercase.

    class Meta:
        db_table = 'person_summary'
