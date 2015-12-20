
def set_user_for_sharding(query_set, user_id):
  if query_set._hints == None:
    query_set._hints = {'user_id' : user_id }
  else:
    query_set._hints['user_id'] = user_id
