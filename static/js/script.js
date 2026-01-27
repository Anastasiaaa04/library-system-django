
$(document).ready(function() {

    $('[data-bs-toggle="tooltip"]').tooltip();


    $('[data-bs-toggle="popover"]').popover();


    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70
            }, 1000);
        }
    });


    $('form').each(function() {
        $(this).on('submit', function(e) {
            var isValid = true;
            $(this).find('[required]').each(function() {
                if (!$(this).val()) {
                    isValid = false;
                    $(this).addClass('is-invalid');
                } else {
                    $(this).removeClass('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Пожалуйста, заполните все обязательные поля');
            }
        });
    });


    $('.alert').not('.alert-danger').delay(5000).fadeOut(500);


    $('[data-confirm]').on('click', function(e) {
        if (!confirm($(this).data('confirm'))) {
            e.preventDefault();
            return false;
        }
    });

    // Update rating display
    $('input[type="range"]').on('input', function() {
        $(this).next('.form-control-plaintext').val($(this).val());
    });

    // File input preview
    $('.form-control[type="file"]').on('change', function() {
        var fileName = $(this).val().split('\\').pop();
        if (fileName) {
            $(this).next('.form-label').text('Выбран файл: ' + fileName);
        }
    });

    // Search form auto-submit on enter
    $('.search-form').on('keypress', function(e) {
        if (e.which === 13) {
            $(this).submit();
        }
    });

    // Initialize Bootstrap tooltips on dynamically created elements
    $(document).on('mouseenter', '[data-bs-toggle="tooltip"]', function() {
        $(this).tooltip('show');
    });

    // Prevent double form submission
    $('form').on('submit', function() {
        var $submitBtn = $(this).find('button[type="submit"]');
        if ($submitBtn.data('submitted')) {
            return false;
        }
        $submitBtn.data('submitted', true);
        $submitBtn.prop('disabled', true);
        $submitBtn.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Отправка...');

        // Re-enable button after 3 seconds if no response
        setTimeout(function() {
            $submitBtn.prop('disabled', false);
            $submitBtn.html('Отправить');
            $submitBtn.removeData('submitted');
        }, 3000);
    });
});