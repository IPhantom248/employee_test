function printResult(response) {
    console.log('begin printing result\n')
    let $tableBody = $("tbody")
    $tableBody.empty()
    if (response.results.length > 0) {
        for (let i = 0; i < response.results.length; i++) {
            let parent = 'Boss'
            if (response.results[i].parent) {
                parent = response.results[i].parent.full_name
            }
            $tableBody.append('<tr>\n' +
                '<th scope="row">' + response.results[i].pk + '</th>\n' +
                '<td>' + response.results[i].full_name + '</td>\n' +
                '<td>' + parent + '</td>\n' +
                '<td>' + response.results[i].salary + '</td>\n' +
                '<td>' + response.results[i].hired_at + '</td>\n' +
                '<td>' + response.results[i].level + '</td>\n' +
                '<td><img class="rounded-circle article-img" src="' + response.results[i].image + '"></td>\n' +
                '<td>\n' +
                '<a href="/employees/'+ response.results[i].pk +'/edit">edit</a><br>' +
                '<a href="/employees/'+ response.results[i].pk +'/delete">delete</a>' +
                '</td>' +
                '</tr>'
            )
        }
        $pagination = $('.pagination')
        $pagination.empty()
        if (response.count > 1){

            console.log(response.data)
            console.log(response.links['previous'])
            $pagination.append('<li class="page-item ' + (response.links['previous'] ? '': 'disabled') + '"><a class="page-link" href='+ (response.links['previous'] ? response.links['previous']: '#') +'>Previous</a></li>')

            for (let i = response.current_page-2; i<response.current_page+5 && i<response.count+1; i++){
                if (i>0){
                        if ($pagination.children().length > 5 ){
                        break
                    }
                        pageHref =
                    $pagination.append('<li class="page-item '+ (response.current_page === i ? 'active': '')  +'"><a class="page-link" href=""> '+ (i) +' </a></li>')

                }

            }
            $pagination.append('<li class="page-item ' + (response.links['next'] ? '': 'disabled') + '"><a class="page-link" href='+ (response.links['next'] ? response.links['next']: '#') +'>Next</a></li>')
            console.log($('.page-item:contains(1)'))
        }

    } else {
        $tableBody.append("<div>Ничего не найдено</div>")
    }
}

$('body').on('click', '.page-item', function (event) {
    event.preventDefault()
    console.log('begin')
    console.log(event.target.href)
    $.ajax({
        url: event.target.href,
        type: 'get',
        success: function (response) {
            let $tableBody = $("tbody")
            $tableBody.empty()
            console.log('success result')
            console.log(response.results[0])
            if (response.results.length > 0) {
                printResult(response)
            }
        }
    })
})

$('#search-form').submit(function (e) {
    e.preventDefault();
    let searchData = $(this).find('#search-input').val();
    console.log(searchData);
    $.ajax({
        url: "{% url 'employees-api' %}",
        type: 'get',
        data: {s: searchData},
        success: function (response) {
            let $tableBody = $("tbody")
            $tableBody.empty()
            printResult(response)
        }
    })
})

$('.top_raw').click(function (e) {
    let a = "8";
    console.log(a);
    e.preventDefault();
    let order_by = $(this).attr('href');
    let searchData = $('#search-form').find('#search-input').val();
    if ($('th').find('input').prop('checked') == true){
        order_by = '-' + order_by
    }
    console.log(order_by);
    $.ajax({
        url: "{% url 'employees-api' %}",
        type: 'get',
        data: {order_by: order_by,
        s: searchData},
        success: function (response) {
            printResult(response)
        }
    })
})

$('th').find('img').click(function(){
    if ($('th').find('input').prop('checked') == true){
        $('th').find('img').attr('src', "../../../static/employee/filterDU.svg")
    } else { $('th').find('img').attr('src', "../../../static/employee/filterUD.svg")
    }
})  
