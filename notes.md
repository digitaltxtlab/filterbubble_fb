# notes for project development #

## data ##
1. hvorfor er status NaN  --> run experiment

2. status (column 5) post kan være repost

3. status update er ofte tomme

4. explain  

5. picture ids are the easiest, but

photos/:
'https://www.facebook.com/417846588273472/photos/a.422220907836040.98251.417846588273472/697918603599601/?type=1'
'a.422220907836040.98251.417846588273472' -> from browser

fbid:
'https://www.facebook.com/photo.php?fbid=10203170212633797&set=gm.686295091430283&type=1'
'fbid=10203170212633797' --> from app

hashlib - hash value

## metadata ##
1. friendship graph? (ground truth)  
   - get

## design ##
1. normalized edit distance between all posts for one --> edit distance matrix (text reuse)
2. cluster topics
3. topic model for each post and KL divergence
4. edit distance on fbid and kld on status (text reuse)
5. sequence alignment (text reuse)
