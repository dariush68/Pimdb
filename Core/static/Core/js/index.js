let movieSliderList = ''

const getMovieSlider = () => {
    console.log("--load movie list --")

    axios.get('/api/v1/Movie/?page_size=15&ordered_by=latest')
        .then(response => {
            console.log(response)

            let movies = response.data.results
            movieSliderList = response.data.results

            // return
            // $("#multiItemSlider").empty()


            movies.map(movie => {
                //console.log("add ", JSON.stringify(movie))

                $("#multiItemSlider").prepend(`
                    <div class="movie-item">
                        <div class="mv-img">
                            <a href=""><img src="${movie.image}" alt="" style="width: 285px; height: 437px" ></a>
                        </div>
                        <div class="title-in">
                            <div class="cate">
                                <span class="blue"><a href="#">Sci-fi</a></span>
                            </div>
                            <h6><a href="#">${movie.title}</a></h6>
                            <p><i class="ion-android-star"></i><span>${movie.rate}</span> /10</p>
                        </div>
                    </div>

                `)
            })

            var multiItemSlider = $('.slick-multiItemSlider');
            multiItemSlider.slick({
                infinite: true,
                slidesToShow: 4,
                slidesToScroll: 4,
                arrows: false,
                draggable:true,
                autoplay: true,
                autoplaySpeed: 5000,
                dots: true,
                responsive: [
                    {
                        breakpoint: 1024,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 3,
                            infinite: true,
                            dots: true
                        }
                    },
                    {
                        breakpoint: 768,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 2
                        }
                    },
                    {
                        breakpoint: 480,
                        settings: {
                            slidesToShow: 1,
                            slidesToScroll: 1
                        }
                    }
                ]
            });

        })
        .catch(error => {
            console.log(error.response)
        })
}
// getMovieSlider()


//-- Most popular Movies --//
const getPopularMovieSlider = () => {

    axios.get('/api/v1/Movie/?ordered_by=download_count')
        .then(response => {
            console.log(response)

            let movies = response.data.results

            // return
            // $("#slick-multiItem-populate").empty()

            movies.map(movie => {
                //console.log("add ", JSON.stringify(movie))

                $("#slick-multiItem-populate").prepend(`
                    <div class="slide-it">
                        <div class="movie-item">
                            <div class="mv-img">
                                <img src="${movie.poster}" alt="" style="width: 185px; height: 284px">
                            </div>
                            <div class="hvr-inner">
                                <a  href="moviesingle.html"> Read more <i class="ion-android-arrow-dropright"></i> </a>
                            </div>
                            <div class="title-in">
                                <h6><a href="#">${movie.title}</a></h6>
                                <p><i class="ion-android-star"></i><span>${movie.rate}</span> /10</p>
                            </div>
                        </div>
                    </div>
                    
                `)
            })

            var multiItemSlider = $('.slick-multiItemSlider');
            multiItemSlider.slick({
                infinite: true,
                slidesToShow: 4,
                slidesToScroll: 4,
                arrows: false,
                draggable:true,
                autoplay: true,
                autoplaySpeed: 2000,
                dots: true,
                responsive: [
                    {
                        breakpoint: 1024,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 3,
                            infinite: true,
                            dots: true
                        }
                    },
                    {
                        breakpoint: 768,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 2
                        }
                    },
                    {
                        breakpoint: 480,
                        settings: {
                            slidesToShow: 1,
                            slidesToScroll: 1
                        }
                    }
                ]
            });

        })
        .catch(error => {
            console.log(error.response)
        })
}
// getPopularMovieSlider()
