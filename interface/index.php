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

				<option value="SELECT `countryformalname`, SUM(`price`) FROM `countries` NATURAL JOIN `summaries` NATURAL JOIN `owned` NATURAL JOIN `details` WHERE `is_free` = 0 GROUP BY `countryformalname` ORDER BY SUM(`price`);">
					Mostrar o nome do país seguido de o total gasto (em centavos) por jogos não gratis
				</option>

				<option value="SELECT `appid` FROM `details` WHERE `linux_support` = 1 AND `appid` NOT IN (SELECT DISTINCT `appid` FROM `news`);">
					Mostrar os appid dos jogos que possuem suporte para linux e não possuem alguma notícia
				</option>
				
				<option value="SELECT `appid` FROM `details` WHERE `linux_support` = 1 AND `mac_support` = 1 AND `windows_support` = 1 ORDER BY `appid`;">
					Mostrar o appid dos jogos que possuem suporte para todas as plataformas (linux, mac e windows)
				</option>
				
				<option value="SELECT `avatarmedium`, `steamid`, `personaname`, MAX(`playtime_forever`), `appid` FROM `summaries` NATURAL JOIN `owned` GROUP BY `steamid`">
					Mostrar o id, nome e avatar de cada jogador e o id do jogo que ela mais jogou
				</option>
				
				<option value="SELECT `appid`, `header_image`, COUNT(`steamid`), SUM(`playtime_forever`) FROM `summaries` NATURAL JOIN `owned` GROUP BY `appid`;">
					Mostrar o id, a imagem, o total de players e o total de tempo jogado de cada jogo
				</option>
				
				<option value="SELECT c1.`countryformalname`, aux.`id`, aux.`nome`, MAX(aux.`total`), aux.`avatarmedium` FROM (SELECT s.`steamid` AS id, s.`personaname` AS NOME, s.`loccountrycode` AS loccountrycode, COUNT(pa.`achieved`) AS total FROM `summaries` s NATURAL JOIN `playerachievements` pa GROUP BY s.`steamid`) aux NATURAL JOIN `countries` c1 GROUP BY c1.`countryformalname` ORDER BY MAX(total);">
					Mostrar o nome do país e o nome e avatar do habitante que mais possui achievements
				</option>
				
				<option value="SELECT D.`appid`, D.`dev_name` FROM `developers` D JOIN `publishers` P ON D.`appid` = P.`appid` AND D.`dev_name` = P.`pub_name` ORDER BY D.`appid`;">
					Selecionar os jogos que possuem desenvolvedores e publicadores iguais
				</option>
				
				<option value="SELECT `steamid1`, `steamid2`, a.`appid` FROM `friends`, `owned` a, `owned` b WHERE a.`steamid` = `steamid1` AND b.`steamid` = `steamid2` AND a.`appid` = b.`appid` ORDER BY `steamid1`;">
					Para cada pessoa selecionar todos os amigos que possuem jogos em comum e mostrar o id do jogo
				</option>
				
				<option value="SELECT `steamid`, `personaname`, CASE WHEN SUM(`price`) > 10000 THEN &quot;verdadeiro&quot; ELSE &quot;falso&quot; END AS verdadeiro_ou_falso FROM `summaries` NATURAL JOIN `owned` NATURAL JOIN `details` WHERE `is_free` = 0 GROUP BY `steamid`;">
					Mostrar &quot;verdadeiro&quot; se uma pessoa gastou mais que R$ 100,00 em jogos e &quot;falso&quot; caso contr&aacute;rio
				</option>
				
				<option value="SELECT `steamid`, `personaname`, `header_image` FROM `summaries` NATURAL JOIN `owned` NATURAL JOIN `details` WHERE `playtime_2weeks` > 0 AND `supported_languages` LIKE '%Portuguese%';">
					Se a pessoa jogou um jogo com suporte para l&iacute;ngua portuguesa nas &uacute;timas duas semanas, exibir steamid e nome da pessoa e imagem do jogo
				</option>
				
				<option value="SELECT c.`countryformalname`, COUNT(DISTINCT d.`appid`) / aux.total FROM `countries` c NATURAL JOIN `summaries` s NATURAL JOIN `owned` o NATURAL JOIN `details` d NATURAL JOIN (SELECT c1.`loccountrycode`, COUNT(DISTINCT s1.`steamid`) AS total FROM `countries` c1 NATURAL JOIN `summaries` s1 GROUP BY c1.`loccountrycode`) aux WHERE d.`is_free` = 0 GROUP BY c.`countryformalname`;">
					Mostrar a porcentagem de jogadores que pagaram por algum jogo para cada país
				</option>
				
				<option value="SELECT c.`countryformalname`, AVG(aux.totalpessoa) FROM `countries` c NATURAL JOIN (SELECT s.`loccountrycode`, SUM(d.`price`) AS totalpessoa FROM `summaries` s NATURAL JOIN `owned` o NATURAL JOIN `details` d WHERE d.`price` > 0) aux GROUP BY c.`countryformalname` ORDER BY c.`countryformalname`;">
					Mostrar a média de dinheiro (em centavos) gasto por pessoa por cada país
				</option>
				
				<option value="SELECT `personaname`, `appid` FROM `summaries` NATURAL JOIN `owned` NATURAL JOIN `details` WHERE `playtime_forever` = 0 AND `price` > 0 ;">
					Selecionar o nome das pessoas e seus jogos comprados que n&atilde;o foram jogados
				</option>
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
