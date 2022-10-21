let movieSliderList = ''

const getCelebritySlider = () => {
    console.log("--load movie list --")

    let actor_id = $("#actor-id").val()

    axios.get('/api/v1/Actor/'+ actor_id + '/')
        .then(response => {
            console.log('r: ', response)

            let actor = response.data

            console.log(actor.image)
            $("#actor-single-img").attr("src", actor.image);

            $("#actor-single-title").empty()
            $("#actor-single-title").append(actor.name + ' ' + actor.family);

            let movieCasts = actor.movieCasts;
            let cast_list = [];
            $("#actor-single-cast").empty()
            movieCasts.map(movieCast => {
                cast_list.push(movieCast.cast_title);
            });
            $("#actor-single-cast").text(cast_list.join(' | '))

            $("#actor-single-abstract").text(actor.bio.substr(0, 300) + " ... ")

            let actorPosters = actor.actorMoviePosters;
            let actorTrailers = actor.actorMovieTrailers;
            //$("#movie-single-gallery").empty();

            actorPosters.map(actorPoster => {
                $("#actor-single-gallery").append(`
                    <a class="img-lightbox"  data-fancybox-group="gallery" href="${actorPoster.moviePoster_poster.replace('http://127.0.0.1:8000/', '')}" >
                    <img src="${actorPoster.moviePoster_poster}" alt="${actorPoster.actor_name}" style="width: 100px; height: 100px; object-fit: cover">
                    </a>
                `);
            });
            actorTrailers.map(actorTrailer => {
                $("#actor-single-gallery").append(`
                    <div class="vd-it">
                        <img class="vd-img" src="images/uploads/play-vd.png" alt="" style="width: 100px; height: 100px; object-fit: cover">
                        <a class="fancybox-media hvr-grow" href="${actorTrailer.movieTrailer_trailer}"><img src="images/uploads/play-vd.png" alt=""></a>
                    </div>
                `);
            });


            movieCasts.map(movieCast => {
                $("#actor-single-films-container").prepend(`
                    <div class="cast-it">
                        <div class="cast-left cebleb-film">
                            <img src="${movieCast.movie_url}" alt="" style="width: 55px; height: 80px; object-fit: cover">
                            <div>
                                <a href="#">${movieCast.movie_title}</a>
                                <p class="time">${movieCast.role}</p>
                            </div>
                        </div>
                        <p>${movieCast.movie_date.split("-")[0]}</p>
                    </div>
                `);
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
getCelebritySlider()
