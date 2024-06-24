const movies = require('../.seed/movies.json')

url = "http://localhost:8000/api/documents/"

async function main(){
    for(const movie of movies){
        await fetch(url, {
            method: "POST",
            body: JSON.stringify(movie),
        })
    }
}

main()