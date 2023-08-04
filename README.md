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
- main template (완성)
  - scss 구축
  - UI/UX 설계
- 유저 경험을 위한 Singup.html 템플릿 정리
  - id 중복검사
```
