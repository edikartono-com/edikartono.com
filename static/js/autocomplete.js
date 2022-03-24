window.addEventListener('load', function(){
	(function($){
		"use strict";
		$('.autocomplete').each(function(){
			let data_url = $(this).attr('autocomplete-url')
			$(this).autocomplete({
				maxLength: 2,
				select: function(event, ui){
					let terms = split(this.value);
					terms.pop();
					terms.push(ui.item.value);
					terms.push('');
					this.value = terms.join(', ');
					return false;
				},
				source: function(request, response){
					let data_abc = split(request)
					$.ajax({
						url: data_url,
						type: 'GET',
						data: data_abc
					}).done(function(respon){
						response($.map(respon, function(el){
							return {
								label: el.name,
								value: el.value
							}
						}))
					})
				},
				multiple: true,
				focus: function(){
					return false;
				}
			});
			
			function split(val) {
				if (val['term']){
					let splt = val['term'].split(', ').pop()
					return {"term": splt}
				} else {
					return val.split(/,\s*/);
				}
			}
		})
	})(django.jQuery);
});