let movieSliderList = ''

const getMovieSlider = () => {
    console.log("--load movie list --")

    let movie_id = $("#movie-id").val()

    axios.get('/api/v1/Movie/'+ movie_id + '/')
        .then(response => {
            console.log('r: ', response)

            let movie = response.data

            console.log(movie.image)
            $("#movie-single-img").attr("src", movie.poster);

            $("#movie-single-title").empty()
            $("#movie-single-title").append(`<span class="ml-2">(${movie.created_on})</span>` + movie.title);

            $("#movie-single-rate").text(movie.rate)
            $("#movie-single-review").text(movie.view_count + ' بازدید ')

            $("#movie-single-star").empty()
            $("#movie-single-star").append(`
                <p>به این فیلم امتیاز دهید:  </p>                
            `);

            let starNum = parseInt(movie.rate);
            for(var i=0; i<starNum; i++){
                $("#movie-single-star").append(`
                <i class="ion-ios-star"></i>                
            `);
            }
            for(var i=starNum; i<10; i++){
                $("#movie-single-star").append(`
                <i class="ion-ios-star-outline"></i>                
            `);
            }

            $("#movie-single-abstract").text(movie.abstract + " ... ")

            let moviePosters = movie.moviePoster;
            let movieTrailers = movie.movieTrailer;
            //$("#movie-single-gallery").empty();

            moviePosters.map(moviePoster => {
                $("#movie-single-gallery").append(`
                    <a class="img-lightbox"  data-fancybox-group="gallery" href="${moviePoster.image.replace('http://127.0.0.1:8000/', '')}" >
                    <img src="${moviePoster.thumbnail}" alt="${moviePoster.movieName}" style="width: 100px; height: 100px; object-fit: cover">
                    </a>
                `);
            });
            movieTrailers.map(movieTrailer => {
                $("#movie-single-gallery").append(`
                    <div class="vd-it">
                        <img class="vd-img" src="${movieTrailer.thumbnail}" alt="" style="width: 100px; height: 100px; object-fit: cover">
                        <a class="fancybox-media hvr-grow" href="${movieTrailer.trailer}"><img src="images/uploads/play-vd.png" alt=""></a>
                    </div>
                `);
            });

            let director = [];
            let writer = [];
            let actors = [];

            let movieCasts = movie.movieCasts;
            $("#movie-single-cast").empty()
            $("#movie-single-stars").empty()
            movieCasts.map(movieCast => {
                if(movieCast.cast_title == "کارگردان") director.push(movieCast.actor_name);
                if(movieCast.cast_title == "نویسنده") writer.push(movieCast.actor_name);

                $("#movie-single-cast").append(`
                <div class="cast-it">
                    <div class="cast-left">
                        <img src="${movieCast.actor_photo}" alt="" style="width: 40px; height: 40px; object-fit: cover">
                        <a href="#">${movieCast.actor_name}</a>
                    </div>
                    <p>${movieCast.role}</p>
                </div> 
                `);

                if(movieCast.cast_title == "بازیگر") {
                    $("#movie-single-stars").append(`
                    <a href="#">${movieCast.actor_name}, </a> 
                    `);
                }

            });

            $("#movie-single-director").text(director.join(','))
            $("#movie-single-writer").text(writer.join(','))
            $("#movie-single-date").text(movie.created_on)
            $("#movie-single-runtime").text(movie.duration)


            let movieGenre = movie.movieGenre;
            $("#movie-single-genres").empty()
            movieGenre.map(movieGenr => {
                $("#movie-single-genres").append(`
                <a href="#">${movieGenr.genre_name}, </a>
                `);
            });


        })
        .catch(error => {
            console.log(error.response)
        })
}
// getMovieSlider()
