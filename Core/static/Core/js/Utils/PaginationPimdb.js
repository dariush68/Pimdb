
//-- confige pagination html element based on REST results --//
function paginationConfige(len, page, page_size, container_title, container) {

    let page_element_count = parseInt((len / page_size) + 1);
    let index_begin = page < 3 ? 1 : page - 2;
    let index_end = page + 2;
    if (page < 3) index_end = 5;
    else if (page + 2 > page_element_count){
        index_end = page_element_count;
        index_begin = page_element_count - 4;
    }
    else index_end = page + 2;

    //-- check page element count --//
    if(page_element_count <= 5){
        index_begin = 1;
        index_end = page_element_count;
    }

    container_title.text(`صفحه از 1 تا ${page_element_count}`);
    container.empty();

    if (page > 1) {
        container.append(`
                    <a onclick='getCelebritiesSmallGrid(1)'><i class="ion-arrow-left-b"></i></a>
                `);
    }

    for (var i = index_begin; i <= index_end; i++) {
        let activeClass = i === page ? `class="active"` : "";
        container.append(`
                    <a href="#" ${activeClass} onclick='event.preventDefault();getCelebritiesSmallGrid(${i})'>${i}</a>
                `);
    }

    if (page < page_element_count) {
        container.append(`
                    <a onclick='getCelebritiesSmallGrid(${page_element_count})'><i class="ion-arrow-right-b"></i></a>
                `);
    }
}
