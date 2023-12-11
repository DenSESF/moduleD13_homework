# Module D13, BulletinBoard - final project

## App "posts" - models for BulletinBoard

* class "Image" - stored Images for advert
  * Method "delet_file" - delete image file and delete folder, if folder empty
* class "Advert" - stored advert
  * Method "delet_file" - delete video file and delete folder, if folder empty
* class "AdvertImage" - ManytoMany relation
* class "Reply" - stored replies for advert

## App "pages"

* class "PostList" - view for all advert with pagination
* class "PostDetail" - view for detail advert, add video and images content
* function "is_owner" - checks the user is the author of the advert
* function "user_directory_path" - create path for storing files
* class "PostDelete" - view for delete advert
* class "PostCreate" - view for create advert
  * class "PostCreateForm" - form for this view
* class "PostEdit" - view for edit advert
  * class "PostUpdateForm" - form for this view, inherit class "PostCreateForm"
* class "ReplyCreate" - view for create reply for advert
  * class "ReplyForm" - form for this view

## App "profiles"

* class "RepliesList" - view for all replies to a user advert
  * class "ReplyFilter" - filter by advert a current user
* function "action_reply" - accept or delete reply

## App "emails" - for sending notify and newsletter a user's

* Add user in group "staff" for permission send newsletter
