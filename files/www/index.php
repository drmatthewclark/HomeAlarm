
<head>
  <meta http-equiv="refresh" content="10">
  <title>Security Control</title>
</head>

<script src="https://code.jquery.com/jquery-1.10.2.js"></script>
<?php include "6dc91608-c991-11e9-a32f-2a2ae2dbcce4-styles.php"  ?>

<?php

 $start = time();
  try {
    $link = pg_pconnect("dbname=alarm user=alarm");

    if (!isset($tlink)) {
      $tlink = pg_pconnect("user=sensor host=pi");
    }
  } catch (Exception $e) {
	echo "Exception ", $e->getMessage(), "\n";
  }


  try {
     $status = pg_exec($link, "select * from state;");
     $nstatus = pg_numrows($status);
     for( $i = 0; $i < $nstatus; $i++) {
        $r = pg_fetch_array($status, $i);
        switch($r["category"]) {
	  case "door alert":
		$da_status = $r["enabled"];
		break;
	  case "alarm-away":
		$alarm_status = $r["enabled"];
		break;
	  case "alarm-stay":
		$home_alarm_status = $r["enabled"];
		break;
	  case "silent-alarm":
		$silent_alarm_status = $r["enabled"];
		break;
	  case "triggered":
		$trigger_status = $r["enabled"];
		break;
	   } 
	} 

  } catch (Exception $f) {
	echo "Exception ", $f->getMessage(), "\n";
  }

  ?>


  <body bgcolor="white">
  <h0>
    Security Control
  </h0>
  <br><br>
  <?php echo date("d M Y h:i a");  ?> 
  <br><br><br>

  <label class="switch" name="door">
     <input type='checkbox' name='door_alert' value='false'  <?php echo $da_status == 't' ? 'checked' : '';?> >
     <span class="slider"></span>
  </label>
  <label for="door_alert" class="chkbox">door alert</label>

  <label class="switch name="alarm">
     <input type='checkbox' name='away_alarm_alert' value='false' <?php echo $alarm_status == 't' ? 'checked' : '';?> >
     <span class="slider"></span>
  </label>
  <label for="away_alarm_alert" class="chkbox">away alarm</label>

  <label class="switch name="alarm">
     <input type='checkbox' name='home_alarm_alert' value='false' <?php echo $home_alarm_status == 't' ? 'checked' : '';?> >
     <span class="slider"></span>
  </label>
  <label for="home_alarm_alert" class="chkbox">at-home alarm</label>

  <label class="switch name="alarm">
     <input type='checkbox' name='silent_alarm' value='false' <?php echo $silent_alarm_status == 't' ? 'checked' : '';?> >
     <span class="slider"></span>
  </label>
  <label for="silent_alarm" class="chkbox">silent</label>
 <br>
  <head>
  <br><br>
  <h1>STATUS:<h1> 

  <?php
     $offline = pg_exec($link, "select source from status where time < (current_timestamp - interval '3 day');");
     $numoffline = pg_numrows($offline);

 	if ($numoffline > 0 ) {
        $list = "";
	echo '<h1>Devices Offline:</h1>';

	for ($i = 0; $i < $numoffline; $i++) {
		$val = pg_fetch_row($offline)[0];
		$list .= $val . ", ";
	}

        $list = substr($list, 0, strlen($list) - 2 );
        echo '<warn>' . $list . '</warn>';
	}

    $open_status = pg_exec($link, "select * from open;");
    $doors_open = pg_numrows($open_status);

    if ($trigger_status == 't') {
      $status =  '<alarm>- ALARM SOUNDING -</alarm>'; 
    } else if ( $doors_open > 0) {
      $status =  '<warn>DOORS/WINDOWS OPEN</warn>'; 
    } else {
      $status =  '<safe>SAFE</safe>'; 
    }
      echo $status;

      echo "<br>";

  if ($doors_open > 0) {
  $result = $open_status;

  echo '<table id="tbl">';
  echo '<tr>';
  echo '<th>Source</th>';
  echo ' <th>Time</th>';
  echo '<th>Event</th>';
  echo '</tr>';

   // Loop on rows in the result set.

   $numrows = pg_numrows($result);
   for($ri = 0; $ri < $numrows; $ri++) {
    echo "<tr>\n";
    $row = pg_fetch_array($result, $ri, PGSQL_ASSOC);
    echo " <td>", $row["source"], "</td>
   <td>", $row["time"], "</td>
   <td>", $row["event"], "</td>
   </tr> ";
   }

   echo "</table>";
   }

  echo "<br><h1>Last Event</h1><br>";

  echo " <table id=\"tbl\">";
  echo "<tr>";
  echo "<th>Source</th>";
  echo "<th>Time</th>";
  echo "<th>Event</th>";
  echo "</tr>";

     $last = pg_exec($link, "select source, time, event  from lastalert where (time::timestamp) > current_timestamp - interval '2 days';");
      // Loop on rows in the result set.
      $numrows = pg_numrows($last);
      for($ri = 0; $ri < $numrows; $ri++) {
         echo "<tr>\n";
        $row = pg_fetch_array($last, $ri, PGSQL_ASSOC);
        echo " <td>", $row["source"], "</td>
        <td>", $row["time"], "</td>
        <td>", $row["event"], "</td>
        </tr>
        ";
      }
    
   echo "</table>";

     $temperature = pg_exec($tlink, "select name, round(temperature::numeric, 1) as t from data where name != 'familyroom2' and time  = (select max(time) from temperature) order by name;");
     $ctime = pg_fetch_array(pg_exec($tlink, "select to_char(max(time), 'HH24:MI') as time from temperature" ))["time"];
     echo "<br><h1>Temperatures at " . $ctime . "</h1><br>";
     echo " <table id=\"tbl\">";
     echo "  <tr>";
     echo "   <th>Name</th>";
     echo "   <th>Temperature &#xb0;F</th>";
     echo "  </tr>";

      // Loop on rows in the result set.
      $numrows = pg_numrows($temperature);
      for($ri = 0; $ri < $numrows; $ri++) {
        echo "<tr>";
        $row = pg_fetch_array($temperature, $ri, PGSQL_ASSOC);
        echo " <td>", $row["name"], "</td><td>",$row["t"],"</td></tr>";
      }
     echo "</table>";

     echo time()-$start;
  ?>
 
 </table>

</br> 

<script>
	$("input[name='door_alert']").change(function(){
	if($(this).is(':checked')) {
		$true_false = true;
	} else {
		$true_false = false;
		$.post('alert_status.php', {var : false, type : 'triggered' });
	}
	var result = $.post('alert_status.php', {var : $true_false, type : 'door alert'}, function(data) { });
	});

	$("input[name='away_alarm_alert']").change(function(){
	if($(this).is(':checked')) {
		$true_false = true;
	} else {
		$true_false = false;
		$.post('alert_status.php', {var : false, type : 'triggered' });
	}
	var result = $.post('alert_status.php', {var : $true_false, type : 'alarm-away'}, function(data) { })
	var result = $.post('alert_status.php', {var : false, type : 'alarm-stay'}, function(data) { })
	});

	$("input[name='home_alarm_alert']").change(function(){
	if($(this).is(':checked')) {
		$true_false = true;	
	} else {
		$true_false = false;
		$.post('alert_status.php', {var : false, type : 'triggered' });
	}
	var result = $.post('alert_status.php', {var : $true_false, type : 'alarm-stay'}, function(data) { });
	var result = $.post('alert_status.php', {var : false, type : 'alarm-away'}, function(data) { });
	});

	$("input[name='silent_alarm']").change(function(){
	if($(this).is(':checked')) {
		$true_false = true;	
	} else {
		$true_false = false;
	}
	var result = $.post('alert_status.php', {var : $true_false, type : 'silent-alarm'}, function(data) { });
	});

</script>

</body>
</html>
