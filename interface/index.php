<!DOCTYPE html>
<html lang="pt_br">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>TP IBD</title>

    <!-- CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/style.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>

 <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a id="nomeProjeto" class="navbar-brand" href="#">TP Banco de Dados</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="index.php">Home</a></li>
            <li class="active"><a href="er.html">Esquema ER</a></li>
            <li class="active"><a href="relacional.html">Esquema Relacional</a></li>
            <li class="active"><a href="grupo.html">Grupo</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">
      	<div class="starter-template">
		    <form action="query.php" method="post">
			<h3>Digite sua query:</h3> <textarea id="text" name="stmt" rows="10" cols="70"> </textarea><br><br>
			<input type="submit">
			</form>
      	</div>
    </div><!-- /.container -->


    <div class="form-group">
      <select class="form-control" id="dropdownlist">
        <option value=""> SELECIONE SUA PESQUISA</option>

        <option value="select countryformalname , sum(price) from countries natural join summaries natural join owned natural join details where is_free = 0 group by countryformalname order by sum(price);">
                      Mostrar o nome do país seguido de o total gasto por jogos não gratis</option>
                      </option>

        <option value="select appid from details where linux_support = 1 and appid not in (select distinct appid from details natural join news);">
                      Mostrar os appid dos jogos que possuem suporte para linux e não possuem alguma notícia</option>
        
        <option value="select appid from details where linux_support = 1 and mac_support = 1 and windows_support = 1 order by appid;">
                      Mostrar o appid dos jogos que possuem suporte para todas as plataformas</option>
        
        <option value="select steamid , personaname  , max(playtime_forever)  , appid from summaries natural join owned natural join details group by steamid;">
                      Mostrar o id da pessoa e o nome e o id do jogo que ela mais jogou</option>
        
        <option value="select appid , count(steamid) , sum(playtime_forever) from summaries natural join owned natural join details group by appid ;">
                      Mostrar o id e o total de players e o total de tempo jogado de cada jogo</option>
        
        <option value="select c1.countryformalname , aux.id , aux.nome , max(aux.total) from (select s.steamid as id, s.personaname as nome , s.loccountrycode as loccountrycode, count(pa.achieved) as total from summaries s natural join playerachievements pa group by s.steamid) aux natural join countries c1 group by c1.countryformalname order by max(total);">
                      Mostrar o nome do país e o nome da pessoa que mais possui achievements</option>
        
        <option value="select appid , dev_name from developers natural join details natural join publishers where pub_name = dev_name order by appid;">
                      Selecionar os jogos que possuem desenvolvedores e publicadores iguais</option>
        
        <option value="select steamid1 , steamid2  , a.appid from friends , owned a, owned b where a.steamid = steamid1 and b.steamid = steamid2 and a.appid = b.appid order by steamid1;">
                      Para cada pessoa selecionar todos os amigos que possuem jogos em comum e mostrar o id do jogo</option>
        
        <option value="select steamid ,  personaname , CASE WHEN sum(price)>100 THEN &quotverdadeiro&quot ELSE &quotfalso&quot END from summaries natural join owned natural join details where is_free = false group by steamid ;">
                      Mostrar verdadeiro se uma pessoa gastou mais que 100$ em jogos e falso caso contrario</option>
        
        <option value="select steamid , personaname , appid from summaries natural join owned natural join details where playtime_2weeks > 0 and supported_languages like '%Portuguese%';">
                      Mostrar o nome da pessoa que jogou um jogo nas últimas 2 semanas que possui suporte para língua portuguesa</option>
        
        <option value="select c.countryformalname ,  count(distinct d.appid) /  aux.total  from countries c natural join summaries s natural join owned o natural join details d natural join (select c1.loccountrycode , count(distinct s1.steamid) as total from countries c1 natural join summaries s1 group by c1.loccountrycode) aux where d.is_free = false group by c.countryformalname;">
                      Mostrar a porcentagem de jogadores que pagaram por algum jogo para cada país</option>
        
        <option value="select c.countryformalname , avg(aux.totalpessoa) from countries c natural join (select s.loccountrycode  , sum(d.price) as totalpessoa from summaries s natural join owned o natural join  details d where d.price > 0) aux group by c.countryformalname order by c.countryformalname;">
                      Mostrar a média de dinherio gasto por pessoa por cada país</option>
        
        <option value="select personaname , appid from summaries natural join owned natural join details where playtime_forever = 0 and price > 0 ;">
                      Selecionar o nome das pessoas e o jogo em que alguem comprou e nao jogou ainda</option>
      </select>
    </div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
    
    <script type="text/javascript">
      var mytextbox = document.getElementById('text');
      var mydropdown = document.getElementById('dropdownlist');

      mydropdown.onchange = function(){
           //mytextbox.value = mytextbox.value  + this.value; //to appened
           mytextbox.innerHTML = this.value;
      }
    </script>

  </body>
</html>
