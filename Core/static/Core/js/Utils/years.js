
//-- fill year --//
function fillYears(selectElement){
    var d = new Date()
    console.log(d.getFullYear())
    let currentYear = d.getFullYear();

    //selectElement = $('#select-actor-birthday-start');

    selectElement.empty();
    selectElement.append(`
        <option value="همه">همه</option>
    `);

    for(let i=0; i<250; i++){
        selectElement.append(`
            <option value="${currentYear-i}">${currentYear-i}</option>
        `);
    }
}