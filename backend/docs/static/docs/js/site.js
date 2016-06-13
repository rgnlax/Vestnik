		function getArticle() {
			var dep = $(".dropdown > .text")[0].innerHTML === 'ЮР' ? $(".dropdown > .text")[0].innerHTML : $(".dropdown > .text")[0].innerHTML + $(".dropdown > .text")[1].innerHTML;
			var article = {
				title: $("input")[0].value,
				udk: $("input")[1].value,
				department: dep,
				reviewer: {
					last_name: $("input")[2].value,
					first_name:$("input")[3].value,
					patronymic:$("input")[4].value,
					email:$("input")[5].value,
					diplom:$("input")[6].value,
					degree:$("input")[7].value,
					post: $("input")[8].value,
				}
			}
			var inputs = $("#authors").children().find("input, .dropdown > .text");
			var authors = []
			for (var j = 0; j < inputs.length; j = j + 8) {
				var author = {
					last_name: inputs[j].value,
					first_name:inputs[j+1].value,
					patronymic:inputs[j+2].value,
					birthday:inputs[j+3].value,
					group:inputs[j+4].value,
					email:inputs[j+5].value,
					phone:inputs[j+6].value,
					post:inputs[j+7].textContent,
				}
				authors.push(author)
			}
			article.authors = authors;
			return article
		}
		function getDocuments() {
			checkboxes = $(".ui.checkbox").checkbox('is checked');
			return {
				"form": checkboxes[0],
				"memo": checkboxes[1],
				"claim": checkboxes[2],
				"review": checkboxes[3],
			}
		}
		function sendData(callback) {
			obj = {
				article: getArticle(),
				documents: getDocuments()
			}
			$.post('documents/generate', JSON.stringify(obj)).done(function(data) {
				callback(data["url"]);
			});
		}
		(function() {
			$('select.dropdown').not("#authors_count").dropdown();
			$('#authors_count').dropdown('setting', 'onChange', function(value, text){
				currentAuthorsCount = $("#authors").children().size();
				diff = value - currentAuthorsCount;
				if (diff < 0) {
					$("#authors").children().slice(diff).remove();
				} else {
					for (var i = 0; i < diff; ++i) {
						var cln= $("#authors > .one.column.row:first").clone().find("input").val("").end();
						$("#authors").append(cln);
					}
					
				}
			});
			$(".ui.checkbox").checkbox('check');
			$(".ui.checkbox").checkbox({onChange: function () {
			$("#documents_count").text("Выбрано: " + $.grep($(".ui.checkbox").checkbox('is checked'), function(i,e){return i === true}).length);
			}})
			$('.coupled.modal').modal({
				allowMultiple: false
			});
			$('#process_button').click(function(){
				$("#documents_modal").modal({onApprove: function() {
					sendData(function(url){
						$("#download_modal").modal("show")
						document.getElementById("url_field").value = location.href + "documents/download/" + url;
					});
					return false;
				}
				}).modal('show')
			})
			$("#download_button").click(function(){
				window.location.href = document.getElementById("url_field").value
			})
		})();