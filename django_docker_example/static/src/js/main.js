//  Hammer é uma variavel global de um script superior
$(".carousel").carousel();
var hammertime = new Hammer($(".painel")[0], {});
hammertime.on("swipe", function(ev) {
  if (ev.offsetDirection === 2) {
    $("a[data-slide='next']").click();
  } else {

    $(".carousel").carousel();
    var hammertime = new Hammer($(".painel")[0], {});
    hammertime.on("swipe", function(ev) {
      if (ev.offsetDirection === 2) {
        $("a[data-slide='next']").click();
      } else {
        $("a[data-slide='prev']").click();
      }
    });
    hammertime.get("swipe").set({direction: Hammer.DIRECTION_HORIZONTAL});

    $($(".carousel-item")[0]).addClass("active");

    $("a[data-slide='prev']").click();
  }
});
hammertime.get("swipe").set({direction: Hammer.DIRECTION_HORIZONTAL});

$($(".carousel-item")[0]).addClass("active");

