(function($){
    "use strict";
    function setCookie(cname, cvalue, exday){
        var c_value = encodeURI(cvalue);
        if(exday){
            var exdate = new Date();
            exdate.setDate(exdate.getDate()+exday);
            c_value += '; expires=' + exdate.toUTCString() + 'SameSite=Lax;secure';
        }
        document.cookie = cname + '=' + c_value;
    }

    function getCookie(cname){
        var i, x, y, cookies = document.cookie.split(';');

        for(i=0; i < cookies.length; i++){
            x = cookies[i].substring(0, cookies[i].indexOf('='));
            y = cookies[i].substring(cookies[i].indexOf('=') +1 );
            x = x.replace( /^\s+|\s+$/g, '' );

            if(x===cname){
                return decodeURI(y);
            }
        }
    }

    let swalShown = false;

    function showPopup(){
        setCookie('shown', true, 1);
        Swal.fire({
            title: "Mau dapat tutorial django melalui email?",
            icon: "question",
            showCancelButton: true,
            cancelButtonText: 'Tidak, sudah ahli!',
            confirmButtonText: 'Ya, saya mau!'
        }).then((result) => {
            if(result.isConfirmed){
                const xyz = '/578e2016-e557-4117-90ce-d4166233eb84/email/contact/create/'
                $.ajax({
                    url: xyz
                }).done(function(respon){
                    swalShown = true;
                    $('#myModal').on('shown.bs.modal', function(){
                        $('#myModal').html(respon);
                        $('#newContact').attr('action', xyz);
                      });
                    $('#myModal').modal({
                        show: true,
                        backdrop: 'static',
                        keyboard: false
                    });
                })
            }
             else if (result.isDismissed){
                swalShown = true;
            }
        })
    };

    var cookie = getCookie('shown');
    if (!cookie){
        $(window).scroll(function(){
            let wH = $(window).height(), wS = $(this).scrollTop();
            
            if ((wS-wH) > 100){
                if(!swalShown){
                    showPopup();
                }
            }
        })
    };
})(jQuery)