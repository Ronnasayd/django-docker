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
