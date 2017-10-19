$(document).ready(function() {
    $('#search_box').on('submit', function(event) {
        $("#table").html("");
        $("#player_name").html("");
        $("#search").html("");
        $.ajax({
                data: {
                    name: $("#name").val()
                },
                type: 'POST',
                url: '/process'
            })
            .done(function(data) {
                if (data.error) {
                    $("#error").html("No Data Available")
                    $("#player_name").html(data.name);
                    $("#age").html("");

                    const stats = {
                        labels: null,
                        series: null,
                    };

                    const myChart = new Chartist.Line('.ct-chart', stats);


                } else if (data.doops == "false") {
                    $("#error").html("")
                    $("#player_name").html(data.name);
                    $("#age").html("Age");
                    $("#key").removeClass('hideMe')
                    const batting_avg = []
                    const all_ages = []
                    const onbase = []
                    const slgPct = []
                    age_data = JSON.parse(data.age)
                    ba_data = JSON.parse(data.avg)
                    obp_data = JSON.parse(data.obp)
                    slg_data = JSON.parse(data.slg)
                    Object.keys(ba_data).forEach(function(key) {
                        const stats = ba_data[key]
                        for (item in stats) {
                            batting_avg.push(stats[item])
                        }
                    });
                    Object.keys(age_data).forEach(function(key) {
                        const ages = age_data[key]
                        for (item in ages) {
                            all_ages.push(ages[item])
                        }
                    });
                    Object.keys(obp_data).forEach(function(key) {
                        const obp = obp_data[key]
                        for (item in obp) {
                            onbase.push(obp[item])
                        }
                    });
                    Object.keys(slg_data).forEach(function(key) {
                        const slg = slg_data[key]
                        for (item in slg) {
                            slgPct.push(slg[item])
                        }
                    });
                    const stats = {
                        labels: all_ages,
                        series: [
                            batting_avg, onbase, slgPct
                        ]
                    };

                    const myChart = new Chartist.Line('.ct-chart', stats);
                }



                if (data.empty == "true") {
                    $("#error").html("No Data");
                }

                if (data.doops == "true") {
                    $("#player_name").html(data.search_name);
                    $("#error").html("")
                    $("#age").html("Age");
                    $("#key").removeClass('hideMe')

                    const batting_avg_search = []
                    const all_ages_search = []
                    const onbase_search = []
                    const slgPct_search = []
                    age_data_search = JSON.parse(data.age_s)
                    ba_data_search = JSON.parse(data.avg_s)
                    obp_data_search = JSON.parse(data.obp_s)
                    slg_data_search = JSON.parse(data.slg_s)
                    Object.keys(ba_data_search).forEach(function(key) {
                        const stats = ba_data_search[key]
                        for (item in stats) {
                            batting_avg_search.push(stats[item])
                        }
                    });
                    Object.keys(age_data_search).forEach(function(key) {
                        const ages = age_data_search[key]
                        for (item in ages) {
                            all_ages_search.push(ages[item])
                        }
                    });
                    Object.keys(obp_data_search).forEach(function(key) {
                        const obp = obp_data_search[key]
                        for (item in obp) {
                            onbase_search.push(obp[item])
                        }
                    });
                    Object.keys(slg_data_search).forEach(function(key) {
                        const slg = slg_data_search[key]
                        for (item in slg) {
                            slgPct_search.push(slg[item])
                        }
                    });
                    const stats_search = {
                        labels: all_ages_search,
                        series: [
                            batting_avg_search, onbase_search, slgPct_search
                        ]
                    };

                    const myChart = new Chartist.Line('.ct-chart', stats_search);
                }

                if (data.server == "false") {
                    $("#error").html("Something Went Wrong.")
                }

                $("#name").val('')

            })


        event.preventDefault();
    });
})