<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { page, is_login } from "../lib/store.js"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    let question_list = []
    let size = 10
    //let page = 0
    let total = 0
    // $: 기호는 반응형 변수가 된다. 즉, total 변수의 값이 API 호출로 인해 그 값이 변하면 total_page 변수의 값도 실시간으로 재 계산된다는 의미
    $: total_page = Math.ceil(total/size)

    function get_question_list() {
        let params = {
            page: $page,
            size: size,
        }
        fastapi('get', '/api/question/list', params, (json) => {
            question_list = json.question_list
            total = json.total
        })

        // fetch("http://127.0.0.1:8000/api/question/list").then((response) => {
        //     response.json().then((json) => {
        //         question_list = json
        //     })
        // })
    }

    // $: 기호는 변수 뿐만 아니라 함수나 구문 앞에 추가하여 사용할 수 있다.
    // $: get_question_list($page)의 의미는 page 값이 변경될 경우 get_question_list 함수도 다시 호출하라는 의미이다.
    $: $page, get_question_list()
</script>

<div class="container my-3">
    <table class="table">
        <thead>
        <tr class="text-center table-dark">
            <th>번호</th>
            <th style="width:50%">제목</th>
            <th>글쓴이</th>
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        {#each question_list as question, i}
        <tr class="text-center">
            <!-- 게시물 번호 공식 : (번호 = 전체 게시물 개수 - (현재 페이지 * 페이지당 게시물 개수) - 나열 인덱스) -->
            <td>{ total - ($page * size) - i}</td>
            <td class="text-start">
                <a use:link href="/detail/{question.id}">{question.subject}</a>
                {#if question.answers.length > 0}
                    <span class="text-danger samll mx-2">{question.answers.length}</span>
                {/if}
            </td>
            <td>{ question.user ? question.user.username : "" }</td>
            <td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
        </tr>
        {/each}
        </tbody>
    </table>
     <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => $page--}">이전</button>
        </li>
        <!-- 페이지번호 -->
        {#each Array(total_page) as _, loop_page}
        {#if loop_page >= $page-5 && loop_page <= $page+5}
        <li class="page-item {loop_page === $page && 'active'}">
            <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
        </li>
        {/if}
        {/each}
        <!-- 다음페이지 -->
        <li class="page-item {$page >= total_page-1 && 'disabled'}">
            <button class="page-link" on:click="{() => $page++}">다음</button>
        </li>
    </ul>
    <!-- 페이징처리 끝 -->
    <a use:link href="/question-create" class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a>
</div>