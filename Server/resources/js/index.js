/*
MIT License

Copyright (c) 2018 LiamZ96

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

//Requirements in this file: 3.2.1, 3.4.1.1
//Authors: Jacob Wakefield, Noah Zeilmann, McKenna Gates

'use-strict'
$(document).ready(function() {
    let singleSubmit = $('#single-submit'),
        multipleSubmit = $('#multiple-submit'),
        imageForm = $('#image-form'),
        videoForm = $('#video-form'),
        cancelImages = $('#cancel-images'),
        cancelVideo = $('#cancel-video'),
        imageUpload = $('#image-upload'),
        videoUpload = $('#video-upload'),
        videoSource = $('#video-src'),
        slideHolder = $('#slide-holder'),
        videoHolder = $('#video-holder'),
        alertContainer = $('#alert-container'),
        crushedBeadCheckbox = $('#crushed-bead-checkbox'),
        overlay = $('#overlay'),
        timeoutMgr = {
            imgFormatTimeout: null,
            videoFormatTimeout: null,
            postTimeout: null,
        }
        prevSrc = null;
    let minBeadValue = document.getElementById('min-bead-value');
    let minSizeSlider = document.getElementById('min-size-slider');

    let maxBeadValue = document.getElementById('max-bead-value');
    let maxSizeSlider = document.getElementById('max-size-slider');

    minBeadValue.innerText = minSizeSlider.value;
    maxBeadValue.innerText = maxSizeSlider.value;

    let colorAlgorithm = document.getElementById('color-algorithm-selection');

    let magSelect = document.getElementById('mag-select');

    minSizeSlider.oninput = function() {
        minBeadValue.innerHTML = this.value;
    }

    maxSizeSlider.oninput = function() {
        maxBeadValue.innerHTML = this.value;
    }

    crushedBeadCheckbox.click(() => {
        crushedBeadCheckbox.toggle(this.checked);
    })


    imageUpload.change(function(e) {
        let invalidFiles;

        cancelImagePreview();

        invalidFiles = Array.from(this.files).filter(function(file) {
            return !(file.name.endsWith('.jpg') || file.name.endsWith('.jpeg'));
        });

        if(this.files.length > 0) {
            if(this.files.length == 1) {
                $('#multiple-submit').addClass('d-none');
                $('#single-submit').removeClass('d-none');
                $('#mag').removeClass('d-none');
            } else {
                $('#multiple-submit').removeClass('d-none');
                $('#single-submit').addClass('d-none');
                $('#mag').addClass('d-none');
            }
        } else {
            $('#multiple-submit').addClass('d-none');
            $('#single-submit').addClass('d-none');
            $('#mag').addClass('d-none');
        }

        if (this.files.length > 0 && invalidFiles.length === 0) {
            if (this.files.length > 1) {
                $('.carousel-control-prev').removeClass('d-none');
                $('.carousel-control-next').removeClass('d-none');
            }

            cancelImages.prop('disabled', false);
            $('#image-label').text(this.files.length + ' images selected');

            $.each(this.files, function(idx, file) {
                let reader = new FileReader();

                reader.onload = function(e) {
                    let carouselItem = $('<div class="carousel-item"></div>'),
                        image = $('<img class="d-block w-100"/>')
                            .attr({
                                src: e.target.result,
                                alt: 'Slide ' + slideHolder.children.length
                            }),
                        caption = $('<div class="carousel-caption d-none d-md-block"></div>'),
                        captionText = $('<span class="caption-text"></span>').text(e.target.fileName);

                    if (idx === 0) {
                        carouselItem.addClass('active');
                        $('#img-placeholder').parent().remove()
                    }

                    caption.append(captionText);
                    carouselItem.append(image);
                    carouselItem.append(caption);
                    slideHolder.append(carouselItem);
                }

                reader.fileName = file.name;
                reader.readAsDataURL(file);
            });
        }
        else if (invalidFiles.length > 0) {
            createAlert('img-alert', 'Only image files of format .jpg and .jpeg are allowed', 'imgFormatTimeout');
            this.value = null;
        }
    });


    cancelImages.click(function() {
        cancelImagePreview();
        $('#multiple-submit').addClass('d-none');
        $('#single-submit').addClass('d-none');
        imageUpload.val(null);
    });


    singleSubmit.click(function() {

        if (imageUpload.val() == null) {
            noImagesSelected();
            return;
        }
        
        let data = new FormData(imageForm[0]);
        let crushedBeadDetection = crushedBeadCheckbox[0].checked;
        let selectedColorAlgorithm = colorAlgorithm.value;
        let magnificationLevel = magSelect.value;
        let url = `/uploadImages?wantsCrushed=${crushedBeadDetection}&colorAlgorithm=${selectedColorAlgorithm}&maglevel=${magnificationLevel}`;

        console.log("URL: " + url);
        overlay.removeClass('d-none');

        $.ajax({
            method: 'POST',
            url: url,
            enctype: 'multipart/form-data',
            data: data,
            cache: false,
            contentType: false,
            processData: false
        })
        .done(function(response) {
            if (response.status === 0) {
                window.location.href = 'getStitchedImage' + response.location;
            }
            else {
                postFail(response);
            }
        })
        .fail(postFail)
    });


    multipleSubmit.click(function() {

        if (imageUpload.val() == null) {
            noImagesSelected();
            return;
        }
        
        let data = new FormData(imageForm[0]);
        let crushedBeadDetection = crushedBeadCheckbox[0].checked;
        let selectedColorAlgorithm = colorAlgorithm.value;
        let url = `/uploadImages?wantsCrushed=${crushedBeadDetection}&colorAlgorithm=${selectedColorAlgorithm}`;

        console.log("URL: " + url);
        overlay.removeClass('d-none');

        $.ajax({
            method: 'POST',
            url: url,
            enctype: 'multipart/form-data',
            data: data,
            cache: false,
            contentType: false,
            processData: false
        })
        .done(function(response) {
            if (response.status === 0) {
                window.location.href = 'getStitchedImage' + response.location;
            }
            else {
                postFail(response);
            }
        })
        .fail(postFail)
    });

    function createAlert(id, msg, mgrId) {
        let alert = timeoutMgr[mgrId] ? $('#' + id) : $('<div id=' + id + ' class="alert alert-danger my-3" role="alert"><strong>Error</strong> ' + msg + '</div>');

        if (timeoutMgr[mgrId]) {
            clearTimeout(timeoutMgr[mgrId]);
        }
        else {
            alertContainer.prepend(alert);
        }

        window.scrollTo(0, 0);

        timeoutMgr[mgrId] = setTimeout(function() {
            alert.remove();
            timeoutMgr[mgrId] = null;
        }, 15000);
    }

    function cancelImagePreview() {
        let placeholder = $('<div class="carousel-item active"><img id="img-placeholder" class="d-block w-100" src="/resources/imgs/no-slides.jpg" alt="No Slides"></div>');

        cancelImages.prop('disabled', true);
        $('.carousel-control-prev').addClass('d-none');
        $('.carousel-control-next').addClass('d-none');
        $('#image-label').text('Choose images');

        while (slideHolder.children().length !== 0) {
            slideHolder.children()[0].remove();
        }

        placeholder.addClass('active');
        slideHolder.append(placeholder);
    }

    function postFail(response) {
        overlay.addClass('d-none');
        createAlert('post-alert', 'An error occured while uploading your files, please try again later.', 'postTimeout');
    }

    function noImagesSelected(e) {
        overlay.addCass('d-none');
        createAlert('no-images-selected', response.msg, 'postTimeout');
    }

});