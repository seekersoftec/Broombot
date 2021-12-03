$(function () {
    (function (window, document) {
        $('a.nation').nationIcon();
        $("#leagueList li a").leagueListEntry();

        $('.simToolTip').tooltip();

        var numMatches = $('#numMatches').val();
        $("#numMatchesLabel").html(numMatches);
        $("#numMatchesSlider").slider({
            max: 12,
            min: 3,
            step: 1,
            value: numMatches,
            slide: function (event, ui) {
                $("#numMatches").val(ui.value);
                $("#numMatchesLabel").text(ui.value);
            }
        });

        var crowdBias = $('#crowdBias').val();
        updateCrowdBias(crowdBias);
        $("#crowdBiasSlider").slider({
            max: 4,
            min: -4,
            step: 1,
            value: crowdBias,
            slide: function (event, ui) {
                updateCrowdBias(ui.value);
            }
        });

        var homeMotivation = $('#homeMotivation').val();
        updateHomeMotivation(homeMotivation);
        $("#homeMotivationSlider").slider({
            orientation: "vertical",
            max: 4,
            min: 0,
            step: 1,
            value: homeMotivation,
            slide: function (event, ui) {
                updateHomeMotivation(ui.value);
            }
        });

        var awayMotivation = $('#awayMotivation').val();
        updateAwayMotivation(awayMotivation);
        $("#awayMotivationSlider").slider({
            orientation: "vertical",
            max: 4,
            min: 0,
            step: 1,
            value: awayMotivation,
            slide: function (event, ui) {
                updateAwayMotivation(ui.value);
            }
        });

        var homeTactics = $('#homeTactics').val();
        updateHomeTactics(homeTactics);
        $("#homeTacticsSlider").slider({
            orientation: "vertical",
            max: 4,
            min: 0,
            step: 1,
            value: homeTactics,
            slide: function (event, ui) {
                updateHomeTactics(ui.value);
            }
        });

        var awayTactics = $('#awayTactics').val();
        updateAwayTactics(awayTactics);
        $("#awayTacticsSlider").slider({
            orientation: "vertical",
            max: 4,
            min: 0,
            step: 1,
            value: awayTactics,
            slide: function (event, ui) {
                updateAwayTactics(ui.value);
            }
        });

        if ($('#nationValue').val().length > 0) {
            $('#' + $('#nationValue').val()).css({
                'backgroundImage': 'url("/images/nations/' + $('#nationValue').val().replace(" ", "") + 'Bold.png")'
            });
            currNation = $('#nationValue').val();
            reloadLeagues(currNation);

            $('#nationLabel span').html(currNation);
            $('#leagueListContainer').css('visibility', 'visible').hide().fadeIn(400);

            if ($('#leagueValue').val().length > 0) {
                $('#leagueListButton').html($('#leagueValue').val() + ' <span class="caret"></span>');
                if ($('#isTournament').val() == 0) {
                    reloadTeams($('#leagueValue').val());
                    $('#homeVsAwayPicker').css('visibility', 'visible').hide().fadeIn(400);
                } else if ($('#isTournament').val() == 1) {
                    reloadRounds($('#leagueValue').val());
                    $('#roundListContainer').fadeIn(400);

                    if ($('#roundId').val() > 0) {
                        $('#roundListButton').html($('#roundValue').val() + ' <span class="caret"></span>');
                        reloadTournamentRoundTeams($('#roundId').val());
                        $('#homeVsAwayPicker').css('visibility', 'visible').hide().fadeIn(400);
                    }
                }

                if ($('#htValue').val().length > 0 && $('#atValue').val().length > 0) {
                    $('#factorPanelSet').fadeIn(400);

                    var matchingHomeValue = $('#ht select option').filter(function () {
                        alert
                        return this.value.toLowerCase() == $('#htValue').val().toLowerCase().replace(" ", "");
                    }).attr('value');
                    $('.htName').text(matchingHomeValue);
                    $('#ht select').val(matchingHomeValue);

                    var matchingAwayValue = $('#at select option').filter(function () {
                        return this.value.toLowerCase() == $('#atValue').val().toLowerCase().replace(" ", "");
                    }).attr('value');
                    $('.atName').text(matchingAwayValue);
                    $('#at select').val(matchingAwayValue);
                }
            } else {
                $('#leagueListButton').html('Select a Competition <span class="caret"></span>');
            }
        }

        $('#matchTypeDropdown li a').matchTypeDropDown();

        $.fn.bootstrapSwitch.defaults.onColor = 'success';
        $("input[name='recentFormCheckBox']").bootstrapSwitch();
        $('input[name="recentFormCheckBox"]').on('switchChange.bootstrapSwitch', function (event, state) {
            if (state) {
                $("#recentFormCheckBox").val('1');
                $("#recentFormValue").val('1');
            } else {
                $("#recentFormCheckBox").val('0');
                $("#recentFormValue").val('0');
            }
        });

    })(window, document);
});

$.fn.nationIcon = function () {
    return this.each(function () {
        var obj = $(this)
        $(this).click(function () {
            var id = $(this).attr('alt');
            var name = $(this).attr('id');
            if (name != currNation) {
                $(this).css({
                    'backgroundImage': 'url("/images/nations/' + name.replace(" ", "") + 'Bold.png")'
                });

                $('#' + currNation).css({
                    'backgroundImage': 'url("/images/nations/' + currNation.replace(" ", "") + '.png")'
                });
                currNation = name;

                reloadLeagues(name);

                $('#nationValue').val(name);
                $('#nationLabel span').html(name);
                $('#homeVsAwayPicker').css('visibility', 'hidden');
                $('#roundListContainer').fadeOut(400);
                $('#leagueListContainer').css('visibility', 'visible').hide().fadeIn(400);
                $('#leagueListButton').html('Select a Competition <span class="caret"></span>');
                $('#factorPanelSet').fadeOut(400);
            }
        });
    });
};

$.fn.leagueListEntry = function () {
    return this.each(function () {
        var obj = $(this)
        $(this).click(function () {
            var id = $(this).attr('id');
            var selText = $(this).text();
            $(this).parents('.btn-group').find('.dropdown-toggle').html(selText + ' <span class="caret"></span>');
            $('#leagueValue').val(selText);

            $('#htValue').val('');
            $('#atValue').val('');
            $('#factorPanelSet').fadeOut(400);

            if ($(this).hasClass('league')) {
                $('#roundListContainer').fadeOut(400);
                $('#isTournament').val(0);

                reloadTeams(id);
                $('#homeVsAwayPicker').css('visibility', 'visible').hide().fadeIn(400);
            } else if ($(this).hasClass('tournament')) {
                reloadRounds(id);
                $('#roundListButton').html('Select a Round <span class="caret"></span>');
                $('#roundListContainer').fadeIn(400);
                $('#isTournament').val(1);
            }
        });
    });
};

$.fn.roundListEntry = function () {
    return this.each(function () {
        var obj = $(this)
        $(this).click(function () {
            var id = $(this).attr('id').substring(5);
            var selText = $(this).text();
            $(this).parents('.btn-group').find('.dropdown-toggle').html(selText + ' <span class="caret"></span>');
            $('#roundId').val(id);
            $('#roundValue').val(selText);

            $('#htValue').val('');
            $('#atValue').val('');
            $('#factorPanelSet').fadeOut(400);

            $('#homeVsAwayPicker').css('visibility', 'visible').hide().fadeIn(400);
            reloadTournamentRoundTeams(id);
        });
    });
};

$.fn.teamListEntry = function () {
    return this.each(function () {
        var obj = $(this)
        $(this).click(function () {
            var id = $(this).attr('id');
            var selText = $(this).text();
            var teamType = $(this).parents('.btn-group').attr('id');
            var otherTeamType = teamType == 'ht' ? "at" : "ht";

            if ($('#' + otherTeamType + 'Value').val() != id) {
                $(this).parents('.btn-group').find('.dropdown-toggle').html(selText + ' <span class="caret"></span>');
                $('#' + teamType + 'Value').val(selText);
                $('#' + teamType + " select").val(id);
                $('#' + otherTeamType + " select option[value=" + id + "]").prop("disabled", true);
                $('#' + otherTeamType + " select option[value!=" + id + "]").prop("disabled", false);
                $('.' + teamType + 'Name').text(selText);

                if ($('#htValue').val().length > 0 && $('#atValue').val().length > 0) {
                    $('#factorPanelSet').fadeIn(400);
                } else {
                    $('#factorPanelSet').fadeOut(400);
                }
            }
        });
    });
};

$.fn.teamDropDownXS = function () {
    $(this).change(function () {
        var id = $(this).find('option:selected').val();
        var selText = $(this).find('option:selected').text();
        var teamType = $(this).parents('.btn-group').attr('id');
        var otherTeamType = teamType == 'ht' ? "at" : "ht";

        $(this).parents('.btn-group').find('.dropdown-toggle').html(selText + ' <span class="caret"></span>');
        $('#' + teamType + 'Id').val(id);
        $('#' + teamType + 'Value').val(selText);
        $('#' + otherTeamType + " select option[value=" + id + "]").prop("disabled", true);
        $('#' + otherTeamType + " select option[value!=" + id + "]").prop("disabled", false);
        $('.' + teamType + 'Name').text(selText);

        if ($('#htValue').val().length > 0 && $('#atValue').val().length > 0) {
            $('#factorPanelSet').fadeIn(400);
        } else {
            $('#factorPanelSet').fadeOut(400);
        }
    });
};

$.fn.matchTypeDropDown = function () {
    return this.each(function () {
        var obj = $(this)
        $(this).click(function () {
            var value = $(this).attr('value');
            var selText = $(this).text();

            $(this).parents('.btn-group').find('.dropdown-toggle').html(selText + ' <span class="caret"></span>');
            $('#matchType').val(value);
        });
    });
};

function reloadLeagues(nation) {
    var xmlhttp;
    if (nation.length == 0) {
        $('#leagueList').html('');
        return;
    }
    if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {// code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.open("GET", "/ajax/loadLeaguesAndTournaments.php?n=" + nation, false);

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            $("#leagueList").html(xmlhttp.responseText);
            $("#leagueList li a").leagueListEntry();
        }
    }

    xmlhttp.send();
}

function reloadRounds(tournamentId) {
    var xmlhttp;
    if (tournamentId.length == 0) {
        $('#roundList').html('');
        return;
    }
    if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {// code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.open("GET", "/ajax/loadRounds.php?t=" + tournamentId, true);

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            $('#roundList').html(xmlhttp.responseText);
            $('#roundList li a').roundListEntry();
        }
    }

    xmlhttp.send();
}

function reloadTeams(competition) {
    $.ajax({
        type: "Get",
        url: "/ajax/loadTeams.php",
        data: "c=" + competition,
        async: false
    }).always(function (data) {
        homeData = data.replace(/\?/gi, "htList");
        homeData = homeData.replace(/\.\.\./gi, "[Select Team]");
        homeData = homeData.replace(/--dropdownCols--/gi, "col-xs-12");
        awayData = data.replace(/\?/gi, "atList");
        awayData = awayData.replace(/\.\.\./gi, "[Select Team]");
        awayData = awayData.replace(/--dropdownCols--/gi, "col-xs-12");
        $('#ht').html(homeData);
        $('#at').html(awayData);

        if ($('#htValue').val().length > 0) {
            $('#htListButton').html($('#htValue').val() + ' <span class="caret"></span>');
            $('#ht select').val($('#htId').val());
            $("#at select option[value=" + $('#htId').val() + "]").attr("disabled", true);
            $("#at select option[value!=" + $('#htId').val() + "]").attr("disabled", false);
        } else {
            $('#htListButton').html('Select Team <span class="caret"></span>');
        }
        if ($('#atValue').val().length > 0) {
            $('#atListButton').html($('#atValue').val() + ' <span class="caret"></span>');
            $('#at select').val($('#atId').val());
            $("#ht select option[value=" + $('#atId').val() + "]").attr("disabled", true);
            $("#ht select option[value!=" + $('#atId').val() + "]").attr("disabled", false);
        } else {
            $('#atListButton').html('Select Team <span class="caret"></span>');
        }

        $('#htList li a').teamListEntry();
        $('#atList li a').teamListEntry();
        $('#ht select').teamDropDownXS();
        $('#at select').teamDropDownXS();
    });
}

function reloadTournamentRoundTeams(roundId) {
    $.ajax({
        type: "Get",
        url: "/ajax/loadTournamentRoundTeams.php",
        data: "r=" + roundId
    }).always(function (data) {
        homeData = data.replace(/\?/gi, "htList");
        homeData = homeData.replace(/\.\.\./gi, "[Select Team]");
        homeData = homeData.replace(/--dropdownCols--/gi, "col-xs-12");
        awayData = data.replace(/\?/gi, "atList");
        awayData = awayData.replace(/\.\.\./gi, "[Select Team]");
        awayData = awayData.replace(/--dropdownCols--/gi, "col-xs-12");
        $('#ht').html(homeData);
        $('#at').html(awayData);

        if ($('#htId').val() > 0) {
            $('#htListButton').html($('#htValue').val() + ' <span class="caret"></span>');
            $('#ht select').val($('#htId').val());
            $("#at select option[value=" + $('#htId').val() + "]").attr("disabled", true);
            $("#at select option[value!=" + $('#htId').val() + "]").attr("disabled", false);
        } else {
            $('#htListButton').html('Select Team <span class="caret"></span>');
        }
        if ($('#atId').val() > 0) {
            $('#atListButton').html($('#atValue').val() + ' <span class="caret"></span>');
            $('#at select').val($('#atId').val());
            $("#ht select option[value=" + $('#atId').val() + "]").attr("disabled", true);
            $("#ht select option[value!=" + $('#atId').val() + "]").attr("disabled", false);
        } else {
            $('#atListButton').html('Select Team <span class="caret"></span>');
        }

        $('#htList li a').teamListEntry();
        $('#atList li a').teamListEntry();
        $('#ht select').teamDropDownXS();
        $('#at select').teamDropDownXS();
    });
}

function updateCrowdBias(val) {
    $("#crowdBias").val(val);

    var description = "";
    if (Math.abs(val) == 1) {
        description = "Slight";
    } else if (Math.abs(val) == 2) {
        description = "Moderate";
    } else if (Math.abs(val) == 3) {
        description = "High";
    } else if (Math.abs(val) == 4) {
        description = "Highest";
    }

    if (val < 0) {
        if ($('#htId').val() > 0) {
            $("#crowdBiasLabel").text($('#htValue').val() + ' - ' + description);
        } else {
            $("#crowdBiasLabel").text('Home Team' + ' - ' + description);
        }
    } else if (val > 0) {
        if ($('#atId').val() > 0) {
            $("#crowdBiasLabel").text($('#atValue').val() + ' - ' + description);
        } else {
            $("#crowdBiasLabel").text('Away Team' + ' - ' + description);
        }
    } else {
        $("#crowdBiasLabel").text('OFF');
    }
}

function updateHomeMotivation(val) {
    $("#homeMotivation").val(val);

    if (val == 0) {
        $('#homeMotivationLabel').text('Lowest');
    } else if (val == 1) {
        $('#homeMotivationLabel').text('Low');
    } else if (val == 2) {
        $('#homeMotivationLabel').text('Normal');
    } else if (val == 3) {
        $('#homeMotivationLabel').text('High');
    } else if (val == 4) {
        $('#homeMotivationLabel').text('Highest');
    }
}

function updateAwayMotivation(val) {
    $("#awayMotivation").val(val);

    if (val == 0) {
        $('#awayMotivationLabel').text('Lowest');
    } else if (val == 1) {
        $('#awayMotivationLabel').text('Low');
    } else if (val == 2) {
        $('#awayMotivationLabel').text('Normal');
    } else if (val == 3) {
        $('#awayMotivationLabel').text('High');
    } else if (val == 4) {
        $('#awayMotivationLabel').text('Highest');
    }
}

function updateHomeTactics(val) {
    $("#homeTactics").val(val);

    if (val == 0) {
        $('#homeTacticsLabel').text('Defensive');
    } else if (val == 1) {
        $('#homeTacticsLabel').text('Patient');
    } else if (val == 2) {
        $('#homeTacticsLabel').text('Normal');
    } else if (val == 3) {
        $('#homeTacticsLabel').text('Direct');
    } else if (val == 4) {
        $('#homeTacticsLabel').text('Attacking');
    }
}

function updateAwayTactics(val) {
    $("#awayTactics").val(val);

    if (val == 0) {
        $('#awayTacticsLabel').text('Defensive');
    } else if (val == 1) {
        $('#awayTacticsLabel').text('Patient');
    } else if (val == 2) {
        $('#awayTacticsLabel').text('Normal');
    } else if (val == 3) {
        $('#awayTacticsLabel').text('Direct');
    } else if (val == 4) {
        $('#awayTacticsLabel').text('Attacking');
    }
}

function loadingIcon() {
    $('#simButton').hide();
    $('#loadingIcon').show();
}