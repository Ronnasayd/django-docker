django2json = function(string_object){
	return JSON.parse(string_object.split("&#39;").join('"'))
};

$('.carousel').carousel();
var hammertime = new Hammer($('.painel')[0], {});
hammertime.on('swipe', function(ev) {
	if(ev.offsetDirection == 2){
		$('a[data-slide="next"]').click();
	}
	else{
		$('a[data-slide="prev"]').click();
	}
});
hammertime.get('swipe').set({ direction: Hammer.DIRECTION_HORIZONTAL });

$($(".carousel-item ")[0]).addClass('active')

var tecnologias = django2json(tecnologias);
console.log(tecnologias);
