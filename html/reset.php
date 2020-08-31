<?php  

// reset alarm that is sounding
$query = "update state set enabled = false where category = 'triggered';";

// log message
$logevent = "insert into actions (action, cause) values ('alarm reset', 'web');";

$link = pg_connect("dbname=alarm user=alarm");
pg_exec($link, $query);
pg_exec($link, $logevent);
pg_close($link);

?>
