from django.db import models



# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
  full_name = models.CharField(max_length=100, blank=True)
  email = models.EmailField(max_length=150)
  bio =models.TextField(null=True)
  profilepic =CloudinaryField('image')
  neighborhood = models.ForeignKey('NeighborHood', on_delete=SET_NULL,null=True, related_name='people', blank=True)
  location =models.CharField(max_length=60,blank=True,null=True)

  def __str__(self):
    return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
  if created:
      Profile.objects.create(user=instance)
  instance.profile.save()
  