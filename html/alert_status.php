<?php  

// toggle enabled switch
$query = "update state set enabled = $_POST[var] where category = '$_POST[type]';";

// log message
$logevent = "insert into actions (action, cause) values ('toggle: $_POST[type] $_POST[var]', 'web');";

$link = pg_connect("dbname=alarm user=alarm");
pg_exec($link, $query);
pg_exec($link, $logevent);
pg_close($link);

?>
