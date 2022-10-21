let celebritiesList = ''

const getCelebrities = () => {
    console.log("--load movie list --")

    axios.get('/api/v1/Actor/')
        .then(response => {
            console.log(response)

            let actors = response.data.results

            // return
            //$("#celebrity-list-container").empty()

            actors.map(actor => {
                //console.log("add ", JSON.stringify(movie))

                $("#celebrity-list-container").prepend(`
                
                <div class="col-md-12">
                    <div class="ceb-item-style-2">
                        <img src="${actor.image}" alt="" style="width: 110px; height: 150px; object-fit: cover">
                        <div class="ceb-infor">
                            <h2><a href="/celebritysingle?id=${actor.id}">${actor.name} ${actor.family}</a></h2>
                            <span>${actor.city_name}, بازیگر</span>
                            <p>${actor.bio.substr(0,300)}</p>
                        </div>
                    </div>
                </div>
                                     
                `)
            })

        })
        .catch(error => {
            console.log(error.response)
        })
}
getCelebrities()
