let movieSliderList = ''

const getMovieSlider = () => {
    console.log("--load movie list --")

    axios.get('/api/v1/Movie/')
        .then(response => {
            console.log(response)

            let movies = response.data.results
            movieSliderList = response.data.results

            // return
            $("#container-movie-list").empty()

            movies.map(movie => {
                //console.log("add ", JSON.stringify(movie))
                let src = $('#url_img_movie_placeholder').attr('data-url');
                if(movie.image){ src = movie.image}

                $("#container-movie-list").prepend(`

                    <div class="movie-item-style-2" dir="rtl">
                        <img src="${src}" alt="" style="width: 220px">
                        <div class="mv-item-infor">
                            <h6><a href="/moviesingle?id=${movie.id}">${movie.title} <span>(${movie.created_on})</span></a></h6>
                            <p class="rate"><i class="ion-android-star"></i><span>${movie.rate}</span> /10</p>
                            <p class="describe" dir="rtl">${movie.abstract}</p>
                            <p class="run-time"> Run Time: ${movie.duration}’    .     <span>MMPA: PG-13 </span>    .     <span>Release: ${movie.created_on}</span></p>
                            <p>Director: <a href="#">Joss Whedon</a></p>
                            <p>Stars: <a href="#">--, </a> <a href="#">--, </a> <a href="#">  --</a></p>
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
