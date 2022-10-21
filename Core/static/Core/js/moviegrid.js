let movieSliderList = ''

const getMovieSlider = () => {
    console.log("--load movie list --")

    axios.get('/api/v1/Movie/')
        .then(response => {
            console.log(response)

            let movies = response.data.results
            movieSliderList = response.data.results

            // return
            $("#container-movie-grid").empty()

            let img_placeholder = $('#img-placeholder').attr('data-url')

            movies.map(movie => {
                //console.log("add ", JSON.stringify(movie))

                $("#container-movie-grid").prepend(`
                    <div class="movie-item-style-2 movie-item-style-1">
                        <img src="${movie.image}" alt="" onerror="this.src='${img_placeholder}';" style="height: 250px; object-fit: cover">
                        <div class="hvr-inner">
                            <a  href="movie/${movie.id}"> Read more 2<i class="ion-android-arrow-dropright"></i> </a>
                        </div>
                        <div class="mv-item-infor">
                            <h6><a href="#">${movie.title}</a></h6>
                            <p class="rate"><i class="ion-android-star"></i><span>${movie.rate}</span> /10</p>
                        </div>
                    </div>                       
                `)
            })

        })
        .catch(error => {
            console.log(error.response)
        })
}
getMovieSlider()
