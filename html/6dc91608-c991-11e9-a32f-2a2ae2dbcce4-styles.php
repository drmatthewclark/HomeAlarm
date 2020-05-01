<style>

alarm {
   color: #000000; 
   background-color: #ff0000;
   display: block;
   text-align: center;
}
warn {
   color: #000000; 
   background-color: #ffff00;
   display: block;
   text-align: center;
}

safe {
   color: #101010; 
   background-color: #00ff00;
   display: block;
   text-align: center;
}


h0   {
  color: black;
  font-family: helvetica;
  font-style: italic;
  font-size: 180%;
  font-weight: bold;
  padding: 30 px;
}

h1   {
  color: blue;
  font-family: verdana;
  font-size: 150%;
  display: block
}


label {
  width:130px;
  display: inline-block;
}

.button {
  background-color: #010CFC; 
  border: none;
  color: white;
  width: 120px;
  padding: 12px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  vertical-align: middle;
  border-radius: 128px;
  transition-duration: 0.2s;
  margin-left: 64px;
}

.button:hover {
  background-color: #40A000; /* Green */
  color: white;
}

.switch {
  position: relative;
  display: inline-block;
  width: 100px;
  height: 34px;
  vertical-align: middle;
}

.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(64px);
  -ms-transform: translateX(64px);
  transform: translateX(64px);
}

.on
{
  display: none;
}

.slider:after
{
 content:'OFF';
 color: white;
 display: block;
 position: absolute;
 transform: translate(-50%,-50%);
 top: 50%;
 left: 50%;
 font-size: 10px;
 font-family: Verdana, sans-serif;
}

input:checked + .slider:after
{  
  content:'ON';
}

#tbl {
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#tbl td, #customers th {
  border: 1px solid #ddd;
  padding: 8px;
}

#tbl tr:nth-child(even){background-color: #f2f2f2;}

#tbl tr:hover {background-color: #ddd;}

#tbl  th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #4CAF50;
  color: white;
}

</style>
