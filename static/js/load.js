function showYoutuber() {
    $.ajax({
        type: 'GET',
        url: '/api/youtuber/all?sample_give=샘플데이터',
        data: {},
        success: function (response) {
            let youtubers = response['youtubers']

            // id, name, photoURL, tags, likes
            for (let i = 0; i < youtubers.length; i++) {
                let id = youtubers[i]['id']
                let name = youtubers[i]['name']
                let photoURL = youtubers[i]['photoURL']
                let tags = youtubers[i]['tags']
                let likes = youtubers[i]['likes']


                let temp_html = `<div class="card" style="width: 18rem;" onclick="showwantYoutuber('${id}')">
                                    <a href="#" >
                                        <img class="card-img"
                                             src="${photoURL}"
                                             alt="Card image cap">
                                        <div class="card-title">${name}</div>
                                    </a>
                                </div>`

                $('#all-cards').append(temp_html)

            }
        }
    });
}

function showTop3Youtuber() {
    $.ajax({
        type: 'GET',
        url: '/api/youtuber/top?sample_give=샘플데이터',
        data: {},
        success: function (response) {
            let youtubers = response['youtubers']

            // id, name, photoURL, tags, likes
            for (let i = 0; i < youtubers.length; i++) {
                let id = youtubers[i]['id']
                let name = youtubers[i]['name']
                let photoURL = youtubers[i]['photoURL']
                let tags = youtubers[i]['tags']
                let likes = youtubers[i]['likes']

                let icon_url = "../static/images/rank-icon-" + (i + 1) + ".png"
                let icon_alt = "rann" + (i + 1)

                let temp_html = `<img src="${icon_url}" alt="&{icon_alt}" class="rank">
                                <div class="card" style="width: 18rem;" onclick="showwantYoutuber('${id}')">
                                    <a href="#" >
                                        <img class="card-img"
                                             src="${photoURL}"
                                             alt="유튜버 사진">
                                        <div class="card-title">${name}</div>
                                    </a>
                                </div>`

                $('#top3-cards').append(temp_html)

            }
        }
    });
}

function showwantYoutuber(id) {
    window.location.href = `/api/youtuber/${id}`

    $.ajax({
        type: "GET",
        url: `/api/youtuber/${id}`,
        data: {},
        error: function (xhr, status, error) {
            alert("에러 발생!");
        },
        success: function (response) {

        }
    })

}