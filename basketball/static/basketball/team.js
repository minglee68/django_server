var loading_nested = 0;

$(function() {
	$(".detail_bottom > button").on('click', function() {
		$("#" + $(this).attr('id').split('_')[0] + "_player_list").slideToggle();
	});
})

function loading_on() {
	loading_nested++;
	if (loading_nested == 1) {
		$("#team_chart").animate({'opacity': 0.3}, 500);
		$("#loading").fadeIn(500);
	}
}

function loading_off() {
	loading_nested--;
	if (loading_nested == 0) {
		$("#team_chart").animate({'opacity': 1.0}, 500);
		$("#loading").fadeOut(500);
	}
}

var chrtdata = {
	labels: ['FG', 'FGA', 'FGP', '3P', '3PA', '3PP', 'FT', 'FTA', 'FTP', 'ORB', 'DRB', 'AST', 'PF', 'ST', 'TOV', 'BS'],
	datasets: [{
		label: 'NBA empty',
		data: [0, ],
		backgroundColor: 'rgba(255, 92, 132, 0.2)',
		borderColor: 'rgba(255, 92, 132, 1)',
		borderWidth: 1,
	}, {
		label: 'KBL empty',
		data: [0, ],
		backgroundColor: 'rgba(54, 162, 235, 0.2)',
		borderColor: 'rgba(54, 162, 235, 1)',
		borderWidth: 1,
	}]
}; // chrt data

window.onload = function() {
	var ctx = document.getElementById('team_chart').getContext('2d');
	window.myChart = new Chart(ctx, {
		type: 'horizontalBar',
		data: chrtdata,
		options: {
			elements: {
				rectangle: {
					borderWidth: 1,
				}
			},
			responsive: false,
			legend: {
				position: 'top',
			},
			title: {
				display: true,
				text: 'Stat'
			}
		}
	}); // chart
} // window.onload
