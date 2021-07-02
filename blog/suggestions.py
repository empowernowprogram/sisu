from .models import Comment, Post, Cluster, PostPreferrence
from users.models import CustomUser
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np
from operator import or_

def update():
      # Create a sparse matrix from user reviews
      all_user_names = map(lambda x: x.username, CustomUser.objects.only("username"))
      all_comment_ids = set(map(lambda x: x.post.pk, Comment.objects.only("post")))
      all_metoo_ids = set(map(lambda x: x.postpk.pk, PostPreferrence.objects.only("postpk")))
          
      all_users = list(all_user_names)
      num_users = len(all_users)
      
      all_ids = all_comment_ids | all_metoo_ids
      
      if all_ids:
         rec_v = dok_matrix((num_users, max(all_ids)+1), dtype=np.float32)
      else:
         rec_v = dok_matrix((num_users, 1), dtype=np.float32)
      
      for i in range(num_users): # each user corresponds to a row, in the order of all_user_names
            user_comments = Comment.objects.filter(author=all_users[i])
            user_metoos = PostPreferrence.objects.filter(username__username__exact=all_users[i])
            
            # if a user has not comment anything, choose the default comments
            if not user_comments:
                user_comments = Comment.objects.filter(pk__in=[1, 2, 3])
            
            # if a user has not metoo anything, choose the default posts
            if not user_metoos:
                user_metoos = PostPreferrence.objects.filter(pk__in=[4, 5, 6])
            
            for user_comment in user_comments:
                rec_v[i,user_comment.post.pk] = user_comment.rec_value
          
            for user_metoo in user_metoos:
                rec_v[i,user_metoo.postpk.pk] = user_metoo.vote_value
      
      #print (rec_v)
      # Perform kmeans clustering
      k = int(num_users / 100) + 2
      kmeans = KMeans(n_clusters=k)
      clustering = kmeans.fit(rec_v.tocsr())      
      
      # Update clusters
      Cluster.objects.all().delete()
      new_clusters = {i: Cluster(name=i) for i in range(k)}
      for cluster in new_clusters.values(): # clusters need to be saved before refering to users
          cluster.save()
       
      for i,cluster_label in enumerate(clustering.labels_):
        new_clusters[cluster_label].users.add(CustomUser.objects.get(username=all_users[i]))

def update_clusters(to_add_new):
    print("In update clusters")
    num_comments = Comment.objects.count()
    update_step = ((num_comments/100)+1) * 5
    
    if to_add_new == "true":
      update()
   
    else:
      if num_comments % update_step == 0: 
        update()
   