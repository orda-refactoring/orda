# 2023/07/17
1. AWS 배포 과정 기록하기(TIL)

2. 새로운 메인 인덱스 페이지 추가

3. 검색 기능 고도화, 추천 기능 추가 

4. 정보 정확도(난이도, 소요시간, 거리, 코스명)

5. 리팩토링 

6. 반응형 만들기

7. 보안, 인증

8. 레벨링 기능 수정

9. 용어 변경, ck editor 변경


# 2023/07/18 
- 장하늬 
```
- 원격 서버에 존재하는 DB를 리팩토링 시 활용하기 위해 백업.
- 원격 서버의 백업 파일을 로컬로 전송하기 위해  SCP를 이용했지만, 권한 문제로 실패함. 원인 분석 중.
```

- 최지원
```
모바일 사용자들의 편의성을 위한 반응형 웹 디자인 정리
  - nav 
  - post index
```

# 2023/07/19
- 공통
```
추천 기능 논의
```
- 장하늬 
```
추후 배포를 위한  CI/CD, DOCKER, RDS 개념 공부
```

- 최지원
```
모바일 사용자들의 편의성을 위한 반응형 웹 디자인 정리
  - footer 
  - main index

가시성을 위한 UI 정리
  - post index
```

# 2023/07/20
- 공통
```
추천 기능 논의
```
- 장하늬 
```
배포 위한 SSL 강의 듣기
새로운 기능 요구사항 분석
  - 유저 맞춤형 메인 페이지: not visited mountains 리스트, 초보/고수 산 리스트,  랜덤 유저의 추천 목록 리스트
  - 추천 목록(콜랙션) 기능
  - 나와의 거리 계산 기능
MainView 작성 중
  - not visited mountains 리스트 구현함
```

- 최지원
```
모바일 사용자들의 편의성을 위한 반응형 웹 디자인 정리
  - posts_index

사용자 가시성을 위한 UI 정리
  - post index
Sass 공부
```

# 2023/07/21
- 공통
```
- 콜랙션 기능 삭제 결정
- 초보/고수 태그 기준 결정
  - 초보: 경사가 낮은, 등산초보
  - 고수: 위험한, 도전적인
```
- 장하늬 
```
- Tag DB 수정
  - '야생동물 출몰' 삭제
  - '도전적인' 추가
- Mountain DB 수정: top_tag 관련 필터 기능 구현시 어려움을 해결하고자 수정함
  - top_tags 프로퍼티 삭제
  - top_tags 필드 추가 및 리뷰 생성 시 자동업데이트 기능 구현
  - 태그 관련 템플릿 수정
```

- 최지원
```
Sass 공부
```

# 2023/07/24
- 장하늬 
```
- Mountain DB 재수정: 새로운 top_tags 필드가 오히려 다루기 어려워, 가상필드로 필터링하고자 원상복귀함.
  - top_tags 프로퍼티 복구
- Main View 기능 구현
  - 랜덤 유저가 좋아요한 산 리스트
  - 초보/고수를 위한 산 리스트
  - 내가 방문하지 않은 산 리스트
```

- 최지원
```
- 코드 유지보수와 재사용을 생각한 scss 정리
  - posts_index

- 모바일 사용자들의 편의성을 위한 반응형 웹 디자인 정리
  - posts_proofshot
```

# 2023/07/25
- 장하늬 
```
- 현 위치와 산 간의 거리 기능 구상 및 구현중
  - 유저의 좌표를 저장하기 위한 UserLocation 모델 생성
  - 유저의 현 위치 저장을 위한 JS 및 VIEW 구현
  - Mountain 모델에 current_location property 작성중
```

- 최지원
```
- 코드 유지보수와 재사용을 생각한 scss 정리
  - posts_search
  - level
  - nav, footer 정리 중

- 가시성을 위한 UI 정리
  - posts_proofshot
```

# 2023/07/26
- 장하늬 
```
- 현 위치와 산 간의 거리 기능 구현 완료
  - current_location 메서드
  - 이에 따른 view 및 template 수정
- 레벨 기존 코드 분석 중
  - 레벨 기능 문제점: 프로필 페이지를 들어가야 user.level이 변동됨
  - 보완하기 위하여 수정 요함
```

- 최지원
```
- 코드 유지보수와 재사용을 생각한 scss 정리
  - nav 완성
  - footer 정리 중
```

# 2023/07/27
- 장하늬 
```
- 레벨 기능 문제점 보완(문제점: 프로필 페이지를 들어가야 level이 변동됨)
  - User모델에 adjust_user_level 메서드 추가
  - 리뷰, 포스트(마이코스) 등 레벨업 관련 view 수정
  - profile view 코드 정리
- 버그 픽스
  - 회원가입 시, userLocation DB도 생성되게 수정함
  - userLocation 관련 오류 발생시, try-except로 관련 필드 none값 할당
- 기계적 가입 방지를 위해 reCAPTCHA 도입 결정
  - 구글 reCAPTCHA 공식문서 읽음
```

- 최지원
```
- 코드 유지보수와 재사용을 생각한 scss 정리
  - footer 완성
  - nav 오류수정
- mainindex 코드 수정
```

# 2023/07/28
- 공통
```
- 현황 검토 시간
  - 최지원
    - scss: 앞으로 일주일 소요 예상
    - 메인 페이지 만든 후 오른 기억 수정 예정
  - 장하늬
    - 보안 강화: 리캡챠 도입 예정
    - 백엔드 리팩토링에 대한 고민
      - 해야할 일: 코드 분할, 용어 정리 중복 코드 제거, CBV와 FBV 중 적합한 뷰로 변환, URL 패턴 관리
      - 테스트, 쿼리최적화 필요성 여부에 대한 고민
```

# 2023/07/31
- 장하늬 
```
- 구글 reCAPTCHA 적용
  - 다만, 유저에게 명확한 정보 전달을 위해 에러 메세지 처리 커스텀 필요
  - 회원가입 폼 내, 다른 유효성 검사도 커스텀 요함(예: 비밀번호의 제한 규칙 설명 알람, 아이디 중복 여부 검사 등)
```

- 최지원
```
- 코드 유지보수와 재사용을 생각한 scss 정리
  - posts_detail
- 모바일 유저들의 UX를 위한 반응형 UI정리
  - posts_detail
  - topbutton
```

# 2023/08/02
- 장하늬 
```
-회원가입 아이디 중복검사 기능 구현중
  - 클라이언트의 정보가 서버로 넘어가지 않는 원인 파악 중
```

- 최지원
```
- main template
  - scss 구축
  - UI/UX 설계
```

# 2023/08/03
- 장하늬 
```
- 최종: 회원가입 보안 및 정보성 강화
  - 구글 reCAPTCHA 도입
  - 아이디 중복 여부 검사 기능 도입
    - 서버 전달되지 않는 원인 찾음: header의 Content-Type을 잘못 씀
    - css 수정(아이디 중복 여부를 통과하지 못할 경우 회원가입 버튼 disabled 활성화)
  - 비밀번호 불일치 안내 문구 삽입
- 로그인 세션 쿠키 만료 기한 설정(3일)
```

- 최지원
```
- main template
  - scss 구축
  - UI/UX 설계
```

# 2023/08/04
- 장하늬 
```
- 접속유저와 산과의 거리 함수(하나의 산, 여러 산) utils 추가
  - 코드 간결함 확보
  - 재사용성 확보
  - 이로 인한 관련 template 및 view 수정
  - main view에 거리 컨텍스트 추가
- config.py -> utils 폴더로 이동 및 level.py로 이름 변경
- 코드 정리
  - 필요 없는 import 및 주석 제거
```

- 최지원
```
- main template (완성)
  - scss 구축
  - UI/UX 설계
- 유저 경험을 위한 Singup.html 템플릿 정리
  - id 중복검사
```

# 2023/08/10
- 장하늬 
```
- mountain_datail View 리팩토링
  -  가독성 및 유지보수 편의를 위해, 함수 분리 및 생성
```

- 최지원
```
- Singup.html 
  - 가독성을 위한 코드 정리
  - 유지보수를 위한 css -> Scss 변경
  - 유저의 가시성을 위한 페이지 정리 (아이디 중복 / catcha 등)
- main.html
  - 유저의 가시성을 위한 페이지 정리 (현 위치와 산과의 거리)
```

# 2023/08/11
- 장하늬 
```
- 리팩토링
  - mountain detail View: weather에 관련되지만 부수적인 함수의 경우, utils.weather.py에 넣고, view에는 중요 함수만 기재하여 가독성을 높임
  -  serializing geodata: 가독성 및 유지보수 편의를 위해, 공간데이터를 직렬화시키는 함수를 생성(모듈화)하여 중복 코드를 줄임(ing)
    - detail View
    - coursedetail View
```

- 최지원
```
-scss를 이용한 코드 재사용성 강화 및 유지보수 강화와 페이지 통일성 증가 / 모바일 유저들을 위한 반응형 웹 디자인
  - accounts_delete
  - accounts_login
  - accounts_passwordchange
  - accounts_update
  - 
- 코드 정리
  - accounts_update
  - accounts_form.scss

-가시성을 증가 (현위치 조회 / 산과의 거리)
  - nav
  - mountain_list
```

# 2023/08/14
- 장하늬 
```
- 리팩토링
  -  serializing geodata: 가독성 및 유지보수 편의를 위해, 공간데이터를 직렬화시키는 함수를 생성(모듈화)하여 중복 코드를 줄임(ing)
    - course_list View
    - 여러 상황에 공통적으로 활용할 수 있는 함수를 만들기 위해, 오히려 해당 함수의 코드가 점점 누더기처럼 되는데...이게 맞나 싶음
  - 데이터 무결성에 대한 고민
    - 소요거리가 0.75km 미만인 경우, 유저에게 유용한 데이터가 아니라고 판단, 해당 레코드들을 모두 삭제하려 했으나, 연결 관계가 복잡하게 얽혀 있어서 무결성에 관련하여 고민요함.
```

- 최지원
```
- scss를 이용한 코드 재사용성 강화 및 유지보수 / 모바일 유저들을 위한 반응형 웹 디자인
  - mountains_mountainsList
  - mountains_search(진행중)
-> 지도 부분의 반응형의 고민 중 :  현재 코드 상태로 보아 감당이 안될 것 같아 특정 크기까지 작아지면 지도 부분을 display:none을 적용하는 것을 논의함
```

# 2023/08/16
- 장하늬 
```
- 리팩토링
  - reset view resource(mountains, courses)에 따라 분할하여 오류 방지
  - sort 함수를 생성하여, 재사용 / 코드 간결화
- filtering and sorting 수정 중
  - 세션으로 pk값을 저장하여 sorting에 대입하는 게 아닌, get으로 url을 쌓아올리는 방법 고민 중  
  
```

- 최지원
```
- scss를 이용한 코드 재사용성 강화 및 유지보수
	- mountains_search(완성)
	- mountains_list 보수
	- mountains_detail(진행중)
- 모바일 유저들을 위한 반응형 웹 디자인
	- mountains_search(완성)
-> mountains_detail 다소 불필요한 코드가 있다고 판단, 내가 짠 코드가 아니라서 코드를 이해하고 줄여나가는 과정 및 반응형에대한 고민을 해봐야겠다.
```

# 2023/08/17
- 장하늬 
```
- 필터와 정렬 기능 전반적 수정
  - 이유
    - 조회 메서드는 get이므로, post로 파라미터를 전달했던 모든 구조를 변경함.
    - 세션에 저장해서 호출하는 방법은 비효율적이며(서버 메모리 낭비), get으로 하면 휘발성인 데이터를 브라우저 및 서버를 종료할 때까지 유지하는 세션으로 이용하는 것은 유저편의성을 저하하므로 수정함.
  - 변경 사항
    - mountain_list, course_all_list 등 정렬과 필터가 포함된 view를 모두 get 메서드로 수정
    - category.js를 추가하여 정렬을 하여도 기존 파라미터를 유지하도록 변경함
    - 세션을 이용하지 않으므로 세션 리셋 기능을 삭제함
- url 패턴 정리
  - post, mountain, account
```

- 최지원
```
- scss를 이용한 코드 재사용성 강화 및 유지보수 / 모바일 유저들을 위한 반응형 웹 디자인
	- mountains_detail(진행중)
-> mountains_detail 다소 불필요한 코드가 있다고 판단 코드를 줄이는 과정을 같이 진행하여 시간이 좀 걸릴 것 같다.
```

# 2023/08/18
- 장하늬 
```
- DB 정리
  - 이유: 0.75km 미만 거리의 등산로는 정보로서 가치가 없다고 판단
  - 조치: 원본 분리 후 불필요한 데이터 삭제한 테이블 생성

- mountainDetailView의 날씨, 미세먼지(&오존), 뉴스 api 수정
  - 이유 및 조치: API 호출을 기다리느라 페이지 전체 로딩 속도가 저하되고 오류 발생시 전체 페이지가 로딩되지 않으므로, mountainDetailView에서 
뉴스 및 날씨관련 api를 분리시키고, 비동기처리를 위해 json으로 데이터 반환하는 함수 생성
  - 비동기 js 코드 짜는 중
  - 추가적으로 API 에러 핸들링요함(간혹 pipe broken이나 api관련 에러가 뜨는 경우, 전체 페이지가 로딩되지 않는 문제 해결위함)
```

- 최지원
```
- scss를 이용한 코드 재사용성 강화 및 유지보수 / 모바일 유저들을 위한 반응형 웹 디자인
	- mountains_detail(진행중)
-> mountains_detail 다소 불필요한 코드가 있다고 판단 코드를 줄이는 과정을 같이 진행하여 시간이 좀 걸릴 것 같다.
```

# 2023/08/22
- 장하늬 
```
- API 비동기화 및 에러 핸들링 완료
  - 비동기 완료
  - 에러 핸들링 코드 추가(try-except)
  - 기타 코드 누락 수정(utils.weather.py - get_direction 함수)

- 메모리 캐싱 공부
  - 우리 프로젝트에 필요한지 여부를 판단하기 위해 해당 개념 공부중
  - 고민 부분
    1. 산이나 등산 코스의 데이터는, 정부에서 해당 등산 코스를 삭제하거나 100대 명산이 변하지 않는 한, 데이터 변경이 이뤄지지 않는 점
    2. 프로젝트의 주요 기능이, 등산 코스나 산의 위치를 확인 하는 read가 빈번한 점
    3. 따라서 매번 DB에서 데이터를 가져 오는 건 서버 비용 낭비라 판단하여 캐싱하는 게 비용을 낮추고 속도를 높힐 수 있지 않나 판단
    4. 하지만 데이터의 양이 메모리의 대부분을 잡아 먹는다면 오히려 성능저하가 일어날 수 있으므로,
    5. 해당 부분을 공부하고, 도입여부를 판단하기로 결정
```

- 최지원
```
- scss를 이용한 코드 재사용성 강화 및 유지보수 / 모바일 유저들을 위한 반응형 웹 디자인
	- mountains_courselist 
	- mountains_detail(진행중)
- 산 상세정보가 없을 경우 오류 수정
댓글 작성 부분에서 반응형의 오류가 있어 레이아웃과 반응형을 고민해 봐야함
-> 날씨 api가 오류가 날 때 대체할 수 있는 이미지를 추가해야함
```

# 2023/08/23
- 장하늬 
```
- 레디스 공부
- 고민 부분
  1. 성능 및 메모리 사용량을 확인을 어떻게 할 것인가?
  2. 어느 부분에 캐싱 할 것인가? (산과 코스 관련 view)
```

- 최지원
```
- scss를 이용한 코드 재사용성 강화 및 유지보수 / 모바일 유저들을 위한 반응형 웹 디자인
	- mountains_detail(진행중)
- 유저의 가시성을 위해 지정 개수 이상의 태그를 선택시 알림창 띄움
- 유저의 가시성을 댓글 작성창의 레이아웃 정리
```

# 2023/08/24
- 장하늬 
```
- 캐싱 도입 및 전후 성능 테스트
  - 일부(detail, course_list) 기능에 캐싱 도입
  - loadtest, locust로 도입 전후 성능 테스트
    - 결과: 대략 5.3초 정도 속도 향상 
	앤드포인트: GET mountains/3/courses/ (총요청수: 1016 / 총유저: 100명 / 증가속도(초) 5명)
	1. 캐싱전
	평균 응답시간: 32103ms (32.103초)
	응답 실패율: 0.1%
	2. 캐싱후
	평균 응답시간: 26753ms (26.753초)
	응답 실패율: 0.1%
    - 보완점: 캐싱하지 않는 데이터가 존재할 경우, db서버 접속 에러(최대 동시 접속자 수 초과)가 발생하므로 쿼리최적화 요함 
```

- 최지원
```
- scss를 이용한 코드 재사용성 강화 및 유지보수 / 모바일 유저들을 위한 반응형 웹 디자인
	- mountains_detail(완료)
- 불필요한 코드 삭제하고 오류가 있는 코드 수정
```

# 2023/08/25
- 장하늬 
```
- 캐싱 전략 선정 고민 및 쿼리 최적화
	- mountain_list 최적화 (쿼리 62개 -> 22개)
	- 조회수 및 좋아요 등 변동사항이 잦은 필드까지 캐싱해야 하는가? 아니면 부분 캐싱해야 할지 전략 선정 중
```

- 최지원
```
mountains_weather
	- scss를 이용한 코드 재사용성 강화 및 유지보수
	- 불필요한 부분 코드 삭제 및 코드 수정
	- 모바일 유저들을 위한 반응형 웹 디자인
	
변경사항으로 수정해야할 부분 / 오류수정(예정)
	- mountains-detail (review, air-img)
	- mountains_weather (스크롤바, 세세한 레이아웃 수정)
```

# 2023/08/28
- 장하늬 
```
- 쿼리 및 캐싱 최적화 진행
```

- 최지원
```
- scss 작성 전 사용중이던 css 파일 삭제
- mountains_detail, mountains_search, base 오류 및 레이아웃 수정
- 코드 재사용성을 높이기 위한 scss 정리 & 모바일 유저들을 위한 반응형 디자인
	- search_region
	- mountains_weather
```

# 2023/08/29
- 장하늬 
```
- 쿼리 및 캐싱 최적화 진행
```

- 최지원
```
- mountains_search오류 수정
- 코드 재사용성을 높이기 위한 scss 정리 & 모바일 유저들을 위한 반응형 디자인
	- accounts_profile (진행중)
	[코드를 100줄 이상 줄임]
```

# 2023/08/30
- 장하늬 
```
- 쿼리 및 캐싱 최적화 진행
```

- 최지원
```
- main_index nav오류 수정
- 코드 재사용성을 높이기 위한 scss 정리 & 모바일 유저들을 위한 반응형 디자인 & 오류 수정
	- accounts_profile (완료)
	[코드를 220줄 줄임]
	- course_detail 작업 시작
```

# 2023/08/31
- 장하늬 
```
- 앱 Mountains 쿼리 최적화 및 캐싱(Redis) 완료
	- mountain_list
		- 개선 전(쿼리 62개, 65.47ms)
		Mean latency:        444.8 ms
		Effective rps:       2
		 
		- 개선 후(쿼리 17개, 39.33ms)
		Mean latency:        282.4 ms
		Effective rps:       4
	
	- mountain_detail
		- 개선 전(쿼리13개, 39.28ms)
		Mean latency:        420.6 ms
		Effective rps:       2
		 
		- 개선 후(쿼리 12개, 37.48ms) / N+1문제 해결
		Mean latency:        307.5 ms
		Effective rps:       3
		 
	- course_list
		- 개선 전(쿼리 15개, 65.24ms)
		Mean latency:        362.8 ms
		Effective rps:       3
	
		- 개선 후(쿼리 4개, 18.27ms)
		Mean latency:        217.9 ms
		Effective rps:       5
	
	-course_all_list
		- 개선 전(쿼리 22개, 33.25ms)
		Mean latency:        284.1 ms
		Effective rps:       4
	
		- 개선 후(쿼리 3개, 21.42ms)
		Mean latency:        213.1 ms
		Effective rps:       5
	
	-course_detail
		- 개선 전(쿼리 6개, 31.62ms)
		Mean latency:        223 ms
		Effective rps:       4
	
		- 개선 후(쿼리 4개, 20.76ms)
		Mean latency:        203 ms
		Effective rps:       5
```

- 최지원
```
- main_index nav오류 수정
- 코드 재사용성을 높이기 위한 scss 정리 & 모바일 유저들을 위한 반응형 디자인
	- course_detail
- 레이아웃 / 오류 수정
	- nav
	- search_region
	- post_index 로그아웃 시 js 일부가 적용이 안되는 오류 수정
- coursesalllist, scss 경량화 작업 남음
```

# 2023/09/04
- 장하늬 
```
- 앱 Posts 쿼리 최적화
	-post_list(index)
		- 개선 전(쿼리 121개, 88.11ms)
		Mean latency:        716.4 ms
		Effective rps:       1
	
		- 개선 후(쿼리 11개, 23.16ms)
		Mean latency:        244 ms
		Effective rps:       4
	-post_detail
		- 개선 전(쿼리 75개, 76.32ms)
		Mean latency:        536.2 ms
		Effective rps:       2
		
		- 개선 후(쿼리 15개, 41.48ms)
		Mean latency:        274.1 ms
		Effective rps:       4
```

# 2023/09/05
- 장하늬 
```
- 앱 Accounts 쿼리 최적화
	- profile
		- 개선 전(쿼리 30개, 54.78ms)
		Mean latency:        309.7 ms
		Effective rps:       3
		
		- 개선 후(쿼리 18개, 40.32ms)
		Mean latency:        251.4 ms
		Effective rps:       4
		
	- my_memories
		- 개선 전(쿼리 111개, 188.80ms)
		Mean latency:        1354.8 ms
		Effective rps:       1
		
		- 개선 후(쿼리 6개, 78. 09ms)
		Mean latency:        465.1 ms
		Effective rps:       2
```

# 2023/09/06
- 장하늬 
```
- MainPage View 쿼리 최적화
	- 개선 전(쿼리 58개 ~ 70개, 약 70ms)
	Mean latency:        443.1 ms
	Effective rps:       2
	- 개선 후(쿼리 8개 ~ 22개, 약 65ms)
	Mean latency:        328.1 ms
	Effective rps:       3
- 캐싱 키 수정(course list)
	- 페이지네이션까지 고려하여 캐싱 키 생성되도록 수정함
- Mountain 모델의 top_tag관련 property 캐싱
	- 매번 불러낼 때마다 손실되는 쿼리 호출 개수를 줄이기위해 캐싱 도입(1시간 마다 만료되도록 함)
```
