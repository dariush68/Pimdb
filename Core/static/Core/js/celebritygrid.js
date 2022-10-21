let celebritiesList = ''

const getCelebrities = () => {
    console.log("--load movie list --")

    axios.get('/api/v1/Actor/')
        .then(response => {
            console.log(response)

            let actors = response.data.results

            // return
            //$("#celebrity-grid-container").empty()

            actors.map(actor => {
                //console.log("add ", JSON.stringify(movie))

                $("#celebrity-grid-container").prepend(`
                <div class="ceb-item">
                    <a href="/celebritysingle?id=${actor.id}"><img src="${actor.image}" alt="" style="width: 270px; height: 400px; object-fit: cover"></a>
                    <div class="ceb-infor">
                        <h2><a href="/celebritysingle?id=${actor.id}">${actor.name} ${actor.family}</a></h2>
                        <span>${actor.city_name}, بازیگر</span>
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
