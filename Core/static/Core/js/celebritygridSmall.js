let celebritiesList = '';

//-- fill birthday years --//
fillYears($('#select-actor-birthday-start'));
fillYears($('#select-actor-birthday-end'));

const getCelebritiesSmallGrid = (page=1, page_size=25) => {

    page_size = parseInt($( "#select-actor-count option:selected" ).val());

    let url = `/api/v1/Actor/?page=${page}&page_size=${page_size}`;

    //-- search term --//
    let searchText = $('#celebrity-search').val();
    if(searchText) url += `&q=${searchText}`;

    let alphabet = $( "#select-actor-alphabet option:selected" ).val();
    if(alphabet && alphabet != 'همه') url += `&alphabet=${alphabet}`;

    let birthday_start = $( "#select-actor-birthday-start option:selected" ).val();
    if(birthday_start && birthday_start != 'همه') url += `&date_from=${birthday_start}-01-01`;

    let birthday_end = $( "#select-actor-birthday-end option:selected" ).val();
    if(birthday_end && birthday_end != 'همه') url += `&date_to=${birthday_end}-01-01`;

    let cast = $( "#select-actor-cast option:selected" ).val();
    if(cast && cast != 'همه') url += `&cast=${cast}`;

    let sort = $( "#celebrity-select-sort option:selected" ).val();
    if(sort) url += `&order=${sort}`;

    console.log(url)

    axios.get(url)
        .then(response => {

            console.log(response)

            //-- pagination -//
            let actors = response.data.results
            let len_actor = response.data.count;
            // return
            $("#actor-count").text(len_actor)


            paginationConfige(len_actor, page, page_size
                ,$("#pagination-celebrity-smallgrid-title")
                , $("#pagination-celebrity-smallgrid"));
            $("#celebrity-grid-small-container").empty()

            actors.map(actor => {
                //console.log("add ", JSON.stringify(movie))
                let city = "";
                if(actor.city_name){
                    city = ',' + actor.city_name;
                }

                if($("#celebrity-grid-small-container").hasClass('large-grid')){
                    console.log("in larg grid")
                    $("#celebrity-grid-small-container").prepend(`
                        <div class="ceb-item">
                            <a href="/celebrity/${actor.id}"><img src="${actor.image}" alt="" style="width: 270px; height: 400px; object-fit: cover"></a>
                            <div class="ceb-infor">
                                <h2><a href="/celebrity/${actor.id}">${actor.name} ${actor.family}</a></h2>
                                <span>${city} بازیگر</span>
                            </div>
                        </div>                                             
                    `)
                }
                else if($("#celebrity-grid-small-container").hasClass('normal-list')){
                    console.log("in list")
                    let shoerBio = "";
                    if(actor.bio_short){
                        shoerBio = actor.bio_short.substr(0,300)
                    }
                    $("#celebrity-grid-small-container").prepend(`
                        <div class="col-md-12">
                            <div class="ceb-item-style-2">
                                <div class="ceb-infor">
                                    <h2>
                                        <a href="/celebrity/${actor.id}">${actor.name} ${actor.family}</a>
                                        <span>${city} بازیگر</span>
                                    </h2>
                                    <p style="margin-top: 10px">${shoerBio}</p>
                                </div>
                                <img src="${actor.image}" alt="" style="width: 110px; height: 150px; object-fit: cover">
                            </div>
                        </div>                                            
                    `)
                }
                else{
                    console.log("in small grid")
                    $("#celebrity-grid-small-container").prepend(`
                    <div class="col-md-4">
                        <div class="ceb-item-style-2">
                            <img src="${actor.thumbnail}" alt="" style="width: 80px; height: 100px; object-fit: cover">
                            <div class="ceb-infor">
                                <h2 style="margin-bottom: 15px"><a href="/celebrity/${actor.id}">${actor.name} ${actor.family}</a></h2>
                                <span>${city} بازیگر</span>
                                <span style="font-family: IRANSansNum"><a href="http://pimdb.ir/admin/Core/actor/${actor.id}/change/" target="_blank"><i class="fa fa-pencil-alt"></i></a></span>
                            </div>
                        </div>
                    </div>
                                         
                    `)
                }

            })

        })
        .catch(error => {
            console.log(error)
            console.log(error.response)
        })
}
getCelebritiesSmallGrid()

//-- change page element count --//
$('#select-actor-count').on('change', function() {

    //-- find current page --//
    //-- bug in last page, page size increase and last page isn't accessible --//
    let selectedPage = 1;
    $('#pagination-celebrity-smallgrid').children('a').each(function () {
        //console.log($(this).text(), $(this).hasClass('active'))
        if($(this).hasClass('active')){
            selectedPage = parseInt($(this).text());
        }
    });

    getCelebritiesSmallGrid(page=1)
});

//-- search --//
const filterActor = () => {
    getCelebritiesSmallGrid();
}


/*$('#celebrity-search').on("input", function() {
    console.log($(this).val())
});*/
