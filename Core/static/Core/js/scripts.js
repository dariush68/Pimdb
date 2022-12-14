new WOW().init();
new SmoothScroll('a[href*="#"]'),
    {
    easing:'linear',
    speed:1000
};

// add name to breadcrumb
//-- used hidden input in base.html to access django url --//
//-- pagination parameters --//
let nextPage = null;
let currentPage = 1;
let itemCount = -1;     //-- total count of item in the database --//
let itemPerPage = 8;   //-- fetched item count in each try --//
let loading = $("#main-page-loading");

console.log("Main Page");
loading.addClass('loading');
$(window).on('scroll load' , function () {
    //console.log("h = " + $(window).scrollTop());
    if  ($(window).scrollTop()>300){

        $('#go-to-top').css('opacity','1').css('visibility' ,'visible');
    }else
        {
        $('#go-to-top').css('opacity','0').css('visibility' ,'hidden');
    }
});

function showProducts(categoryId){
    $("#main-page-product-loading").addClass('loading');
    // if(itemCount !== -1 && (currentPage - 1) * itemPerPage > itemCount){
    //     console.log("ended");
    //     alert("ended");
    //     $("#all-products-show-more").attr('disabled', 'true');
    //     return
    // }
    loading.addClass('loading');
    //-- get browser width --//
    let widthBrowser = $(window).width();
    //-- cal. item per page based on browser width and item width --//
    itemPerPage =(Math.floor( widthBrowser/document.getElementById("temp-item-width").offsetWidth)) * 2;
    $.ajax({
        url: (nextPage === null && currentPage === 1) ? url_company_product : nextPage,
        type: "GET",
        data: {
            'title': "",
            'category': categoryId,
            'page_size': itemPerPage,
        },
        dataType: 'json',
        success: function (data) {
            // console.log(JSON.stringify(data));
            let companyName = [];
            let productTitle = [];
            let companyLocation = [];
            let companyTag = [];
            let productImages = [];
            let productView = $(`#home-${categoryId}-products`);
            let mapMarkerIcon = $(`#url-company-svg-icon`).attr("data-url");
            let url_base = $("#url-base").attr("data-url");
            let result = data["results"];
            nextPage = data["next"];
            itemCount = data["count"];
            currentPage = currentPage + 1;
            result.map(item => {
                companyName.push(item["company"].title);
                companyLocation.push(item["company"].city);
                companyTag.push(item.category.title);

                //-- check pictures count --//
                if(item['pictures'].length > 2){
                    productImages.push(item.pictures);
                }
                else{
                    let itm = fetchParentItem(item);
                    productImages.push(itm.pic);
                }

                if(item["subSubMaterial"] !== null){
                    productTitle.push(item["subSubMaterial"].title)
                }
                else if(item["subMaterial"] !== null){
                    productTitle.push(item["subMaterial"].title)
                }
                else if(item["material"] !== null){
                    productTitle.push(item["material"].title)
                }
                else if(item["materialCategory"] !== null){
                    productTitle.push(item["materialCategory"].title)
                }
                else if(item["baseCategory"] !== null){
                    productTitle.push(item["baseCategory"].title)
                }
                else if(item.category !== null){
                    productTitle.push(item.category.title)
                }
                else {
                    productTitle.push("-")
                }
            });
            for(let i = 0; i < productTitle.length; i++){

                if(result[i]['pictures'].length > 2) {
                    let img = JSON.parse(productImages[i]);
                    var productPicUrl = "";

                    if (img != "") {
                        productPicUrl = url_base.substring(0, url_base.length-1) + img.pic;
                    } else if (companyTag[i] === "??????????") {
                        productPicUrl = "/static/Core/images/MaterialProductIcon.png";
                    } else if (companyTag[i] === "????????????") {
                        productPicUrl = "/static/Core/images/MechanicProductIcon.png";
                    } else if (companyTag[i] === "??????") {
                        productPicUrl = "/static/Core/images/ElectricProductIcon.png";
                    }
                }
                else{
                    var productPicUrl1 = productImages[i];
                }
                let productNameUrl = productTitle[i].split(' ').join('-');
                let companyNameUrl = companyName[i].split(' ').join('-');
                productView.append(
                    `<div class="col-width" style="direction: ltr ; padding: 5px">` +
                        `<div class="card product-card mb-2" style="width: 100%">` +
                            `<div class="media" style="margin: 5px; position: relative; background-color: #f7f7f7">` +
                                //`<a href="${url_base}product/${result[i]["id"]}/${productNameUrl}">` +
                                `<a href="${url_base}${result[i]["id"]}/product/">` +
                                    ((result[i]['pictures'].length > 2) ?
                                    `<img src=${productPicUrl} style="width: 120px ; height: 105px; object-fit: cover" class="align-self-end img-thumbnail"  alt="Responsive">`
                                    :
                                    `<img src=${productPicUrl1} style="width: 120px ; height: 105px; object-fit: cover" class="align-self-end img-thumbnail"  alt="Responsive">`) +
                                `</a>` +
                                `<div class="media-body">` +
                                    `<span class="pr-1  d-block" style="color: #307e88 ; font-size: 14px ; padding-top: 5px" id="product-title">` +
                                        ` ${productTitle[i]} ` +
                                    `</span>` +
                                     `<b class="pr-1 mt-2 d-block" style="color: #336799 ; font-size: 14px ; padding-top: 5px" id="product-title">` +
                                        ` ${companyLocation[i]} ` +
                                        //`<i class="fa fa-map-marker-alt align-middle ml-1"></i>` +
                                        `<img src=${mapMarkerIcon} style="width: 22px; height: 22px" alt="">` +
                                    `</b>` +
                                    `<span onclick="bookmarkProduct(${result[i]["id"]})" class="mr-2 bg-info"><i class="fa fa-bookmark align-middle" id="bookmark-product-${result[i]["id"]}" style="color: rgb(189, 189, 189); font-size: 17px; position: absolute; left: 125px; bottom: 5px; cursor: pointer"></i></span>` +
                                `</div>` +
                            `</div>` +
                            `<div class="card-footer d-flex"  style="font-size: 12px; padding: 6px;color: #307e88;direction: rtl ">` +
                                //`<a href="${url_home}company/${result[i]["company"]["id"]}/${companyNameUrl}" id="company-name">` +
                                `<a href="${url_home}${result[i]["company"]["id"]}/company/" id="company-name">` +
                                    ` ${companyName[i]} ` +
                                `</a>` +
                                `<span class="d-none mr-auto my-auto" style="height: 16px">249<i class="fa fa-eye mr-2"></i></span>` +
                            `</div>` +
                        `</div>` +
                    `</div>`
                );
            }
            $("#main-page-product-loading").removeClass('loading');
        },
    })
}

const bookmarkProduct = productId => {
    console.log(localStorage.getItem('accessToken'))
    let userIsLogin = $("#isLogin").val()
    if (userIsLogin === 'False') {
        let url = $("#login-url").attr('data-url');
        window.location.href = url;
        return
    }
    let bookmark_status = false;
    if ($(`#bookmark-product-${productId}`).css('color') === 'rgb(189, 189, 189)')  /* Grey */ {
        $(`#bookmark-product-${productId}`).css('color', 'rgb(245, 67, 54)')  /* Red */;
        bookmark_status = true;
    }
    else if ($(`#bookmark-product-${productId}`).css('color') === 'rgb(245, 67, 54)'){
        $(`#bookmark-product-${productId}`).css('color', 'rgb(189, 189, 189)');
        bookmark_status = false;
    }
    $.ajax({
            url: url_bookmark_product,
            type: "POST",
            dataType: 'json',
            data: {
                'product': productId,
                'status': bookmark_status,
            },
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
            },
            success: function (response) {
                console.log(JSON.stringify(response));
            },
            error: function (error) {
                console.log(JSON.stringify(error));
            }
        });
        console.log()
};
// $('#search-button').click(function (event) {
//     event.preventDefault();
//     nextPage = null;
//     currentPage = 1;
//     itemCount = -1;
//     $("#product-view").empty();
//     showMore();
// });



// $("#show-more-all-products").click(function () {
//     showProducts()
// });

// $(window).scroll(function(){
//     if (Math.floor($(window).scrollTop()) >= $(document).height() - $(window).height() - 5 && Math.floor($(window).scrollTop()) <= $(document).height() - $(window).height() + 5){
//         showMore()
//     }
// });

