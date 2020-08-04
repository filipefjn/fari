
## frontend
- improve mobile support
  - seekbar
  - rating modal
- footer
  - display rating on current song
- artists view
  - display number of albums, songs, common tags
  - if there are no artists, display a button to begin
- albums view
  - option to add tags to entire album
- filter view
  - add filter by rating (between x an y)
  - implement AND/OR logic on tag inclusion
  - implement tag exclusion
  - order tags alphabetically
  - search tags
- queue view
  - lazy load full queue if long
  - drag and drop to change order
  - add option to remove from queue
- server view
  - add relevant/interesting info
    - number of artists
    - number of albums
    - number of songs
- styling
  - remove scss from within vue components
    - put in scss files instead
  - use classes with prefix instead of scopes
- error handling
  - implement a snackbar for error notifications
- player
  - fetch next song's file before current finishes
- song lists
  - display song duration
  - add option to show/hide columns
  - resizable columns
  - add option to play song next
  - add option to add song to end of queue
- implement an playlist system
  - implement drag and drop
- implement login system
  - login view
  - users view
- keyboard shortcuts
- implement vue router
- add a logo on the left top corner

## backend
- create new APIs more REST-like
- improve library remake/refresh
  - current algorithm is very slow
- implement 'users' and 'user_permissions' tables

## repository
- add development environment setup instructions
- add screenshots
- rename to 'noisephile'
