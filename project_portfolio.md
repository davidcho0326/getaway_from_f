# Anthropic AE 지원 — 코드베이스 프로젝트 포트폴리오

> **지원자**: 조한솔
> **포지션**: Account Executive, Startups — Anthropic Korea
> **문서 목적**: 본인 코드베이스의 실제 프로젝트 중 JD·전략문서·이력서에 가장 부합하는 11개를 선별·분석

---

## 문서 개요

### 선정 기준

공고문의 핵심 요건 6가지를 기준으로, 각 프로젝트가 **최소 2개 이상**을 충족하도록 선별했습니다.

| # | JD 요건 | 약칭 |
|---|---------|------|
| 1 | 3+ years B2B startup sales, consultative approach | **B2B세일즈** |
| 2 | Selling to technical stakeholders, strategic deals | **기술세일즈** |
| 3 | Strategic business advisor to startup founders | **전략어드바이저** |
| 4 | Passion for AI, especially safe/responsible AI | **AI열정** |
| 5 | Analytical + creative market execution | **분석실행** |
| 6 | Korean market expansion | **한국시장** |

### 스토리 아크

전략문서의 핵심 내러티브를 따릅니다:

```
Part 1: "Claude가 처음으로 작동했습니다" → "Claude가 스스로 진화합니다" — Claude/MCP 전문성
        ↓
Part 2: "F&F 200명을 AI 네이티브로 전환" — 엔터프라이즈 AI 시스템
        ↓
Part 3: "스타트업 생태계에 그 경험을 전하겠습니다" — AI 생태계 리터러시 + 기술적 깊이
```

### 탐색 범위

4개 디렉토리, 26개+ 프로젝트를 전수 탐색 후 11개를 선정했습니다.

- `C:\python` (캡셔닝/태깅 자동화 코드)
- `c:\python\venv` (루트 — 26개 프로젝트)
- `D:\comfy\custom_nodes\Linn_node` (ComfyUI 커스텀 노드)
- `D:\python_sub_for_video` (비디오 생성 프레임워크)

---

## Part 1: "Claude가 처음으로 작동했습니다" → "Claude가 스스로 진화합니다"

> 이 섹션은 Anthropic AE로서 가장 직접적인 차별화 포인트입니다.
> "Claude를 팔기 전에, Claude에게 구원받은 사람"이라는 전략문서의 첫 문장을 증명하고,
> 나아가 **"Claude가 스스로 역량을 확장하는 시스템을 만든 사람"**까지 보여줍니다.

---

### 1.1 패션 이미지 태깅 자동화 시스템 — "Claude가 처음으로 작동한 순간"

**한줄 설명**: Claude와 협업하여 비개발자가 직접 구축한 패션 이미지 15만 개 자동 태깅 시스템 — F&F 전사 AI 전환의 기폭제

**디렉토리**: `C:\python\` (Captioning V2_1.py, V3.py, V3_clothes.py, V3_bag_hat_shoes.py 등 7개 파일)

**기술 스택**:
- **코드 생성**: Claude (코딩 어시스턴트 — 비개발자가 Python 코드를 작성하는 데 사용)
- **이미지 분석**: OpenAI GPT-4o Vision API (2단계: 태그 생성 → 택소노미 검증/보정)
- **비디오 분석**: Google Cloud Vision API + GPT-4o (프레임 추출 → 패션 트렌드 감지)
- **데이터 관리**: pandas, Excel 기반 택소노미, 유의어 사전 (영어→한국어 표준 태그 정규화)
- **배치 처리**: 폴더 단위 일괄 처리, 이미지별 .txt 태그 파일 생성

**규모 지표**:
- **15만 개** 패션 이미지 처리 (5일 만에, 비용 90% 절감, 정확도 90%)
- 7개 Python 스크립트, **V2→V3 3세대 진화** (Excel 규칙 기반 → 내장 택소노미 → 품목별 전문화)
- **47개 패션 택소노미 카테고리**: 120+ 의류 타입, 50+ 색상, 41 소재, 27 패턴, 29 신발 타입 등
- 2단계 파이프라인: GPT-4o 태그 생성 → 택소노미 딕셔너리 기반 검증/보정 (환각 방지)
- Excel 유의어 체계: 영어 동의어 → 한국어 대표어 정규화 (예: "t-shirt" → 표준 분류)
- **3가지 전문화 버전**: 의류(V3_clothes), 액세서리(V3_bag_hat_shoes), 범용(V3)

**JD 연결 분석**:

| 연결 대상 | 구체적 매핑 |
|-----------|------------|
| **전략문서 — "Claude가 처음으로 작동했습니다"** | 이 코드가 그 순간의 산출물. "코드를 쓴 적 없는 사람이 Claude와 협업해서 실제 비즈니스 문제를 풀었다" — 추상적 주장이 아니라 실행 가능한 Python 코드 7개로 증명 |
| **공고문 — AI 열정** | Claude를 코딩 어시스턴트로, GPT-4o를 이미지 분석 모델로 — 각 AI의 강점에 맞게 적재적소에 배치하는 판단력. "AI 도구를 아는 것"이 아니라 "어떤 AI를 어디에 쓸지 아는 것" |
| **전략문서 — PoC에서 전사로** | 이 태깅 시스템의 성공이 F&F 경영진을 설득한 첫 데이터. 5일 만에, 비용 90% 절감, 정확도 90% — 이 숫자가 이후 4000만→10억 PoC 확장의 신뢰 기반 |
| **공고문 — B2B 세일즈** | "비개발자도 Claude와 함께 이런 시스템을 만들 수 있다"는 것 자체가 스타트업 고객에게 가장 설득력 있는 세일즈 피치. AE 본인이 살아있는 성공 사례 |
| **이력서 — Varco Art 프로젝트** | 이 태깅 시스템이 Varco Art 모델 훈련용 데이터 품질의 기반. 15만 이미지를 정확하게 분류했기에 이후 이미지 생성 프로젝트가 가능해진 것 |
| **공고문 — 분석적 + 창의적 실행** | 47개 택소노미 설계(분석적) + V2→V3 3세대 진화(창의적) + 2단계 환각 방지 파이프라인(분석적). 이 시스템은 한 번 만들고 끝난 게 아니라 계속 개선해온 결과 |

---

### 1.2 AX팀 Claude Code Skills 플랫폼

**한줄 설명**: 8인 AX팀이 공유하는 Claude Code 커스텀 스킬 생태계 — 스킬 제작·배포·동기화를 자동화

**디렉토리**: `c:\python\venv\CC_ax_team\`, `c:\python\venv\CC_ax_team_skills\`

**기술 스택**: Claude Code Skills (.md), GitHub Actions, Playwright MCP, Git auto-push/sync

**규모 지표**:
- 9+ 전문 스킬 (이미지 생성, Instagram 분석, K-pop SNS 검색, CEO 보고용 PPT, LLM API 문서 수집 등)
- skill-push / skill-sync 자동화 (Claude Code에서 "스킬 푸시해줘" 한마디로 GitHub 업데이트)
- 팀 전원(8명) 실사용, Private GitHub 레포지토리 운영

**JD 연결 분석**:

| 연결 대상 | 구체적 매핑 |
|-----------|------------|
| **공고문 — AI 열정** | Claude Code의 Skill 시스템을 팀 단위로 운영. 단순 사용자가 아니라 Claude 생태계의 확장 기능을 직접 설계하고 배포하는 수준 |
| **전략문서 — Context Architect Training** | 이 스킬 레포가 곧 스타트업 C-Level 교육의 실전 교보재. "Claude를 이렇게 쓰면 됩니다"를 보여줄 때 추상적 설명이 아니라 실제 동작하는 스킬을 시연 |
| **이력서 — 사내 AI 역량 교육** | 150명 교육의 결과물이 이 시스템. 교육 → 스킬 제작 → 팀 공유 → 재교육의 선순환 |
| **공고문 — 기술 이해관계자** | CTO/CPO에게 "Claude Code Skills가 뭔가요?"를 직접 시연하며 설명할 수 있는 역량 |

---

### 1.3 F&F Knowledge Graph — 엔터프라이즈 BI MCP 서버

**한줄 설명**: 37개 의도(Intent) / 29개 API 도구로 전사 매출·SCM·조직 데이터를 Claude가 분석하는 Knowledge Graph 기반 MCP 서버

**디렉토리**: `c:\python\venv\fnf_kg\`

**기술 스택**: MCP Server (FastAPI), Neo4j Knowledge Graph, Snowflake SQL, REST API, Claude Code 연동

**규모 지표**:
- 37개 의도 노드, 29개 API 도구, 9개 스킬 기반 의도
- 5개 브랜드(MLB, Discovery, MLB KIDS, Duvetica, Sergio Tacchini) 매출/SCM/조직 분석
- 일별/주차별/월별/시즌별 시계열 분석 지원
- 프로덕션 서버 운영 중 (`http://10.90.8.101:8000/mcp` — 사내 인트라넷)

**JD 연결 분석**:

| 연결 대상 | 구체적 매핑 |
|-----------|------------|
| **공고문 — 기술 이해관계자 세일즈** | CTO/CPO에게 "MCP가 뭔가요?"를 답할 때, Knowledge Graph → Intent → Tool → SQL이라는 아키텍처를 직접 설계하고 운영한 경험으로 설명 가능 |
| **공고문 — 전략적 비즈니스 어드바이저** | 매출 데이터 기반 의사결정 시스템을 "어떻게 설계하나"를 아는 것. 스타트업 Founder에게 "Claude로 BI를 만들 수 있다"를 PoC로 보여줄 수 있는 역량 |
| **전략문서 — 패션/이커머스 세그먼트** | F&F 5개 브랜드의 실제 매출/재고/상품 데이터를 다룬 경험. 패션 스타트업 고객과 같은 언어로 대화 가능 |
| **이력서 — RAG 챗봇 구축** | 이 KG 시스템이 이력서 "사내 지식 문서 RAG 챗봇"의 진화형. 정보 검색 시간 80% 단축 성과의 기술적 기반 |

---

### 1.4 Autoskill — Claude 자율 스킬 생성 파이프라인

**한줄 설명**: 오픈소스 트렌드 리서치 스킬([last30days](https://github.com/mvanhorn/last30days-skill))로 Reddit·X·YouTube·웹의 최신 기술 트렌드를 자동 수집 → 커스텀 브리지로 스코어링·중복제거 → Claude Code가 스킬을 자율 생성 → 팀 태스크 매칭 → 4패널 다이어그램 시각화까지, **트렌디한 기술을 빠르게 내재화하는 End-to-End 스킬 팩토리**

**디렉토리**: `c:\python\venv\autoskill (1)\` (엔진), `c:\python\venv\trend-bridge\` (입력 브리지)

**전략 테제 — "Claude가 스스로 진화하는 시스템"**:

> 1.2에서 팀원이 수동으로 만든 스킬 생태계를, 이 시스템은 **자동화**합니다.
> 트렌드가 발견되면 → 콘텐츠를 추출하고 → Claude Code가 headless로 스킬을 생성하고 → 팀 업무와 매칭합니다.
> "Claude를 잘 쓰는 사람"에서 **"Claude가 스스로 역량을 확장하는 시스템을 만든 사람"**으로의 도약입니다.
> 특히 오픈소스 커뮤니티 스킬(last30days)을 프로덕션 파이프라인에 통합한 사례로, **Claude Code Skills 생태계를 실전에서 활용하는 방법**을 보여줍니다.

**기술 스택**:
- **파이프라인 엔진**: Python (~2,549 LOC), 5-Stage 자율 파이프라인
- **Claude Code Headless**: `claude -p --output-format json --max-turns 10` (subprocess 호출, 비대화형 자율 실행)
- **콘텐츠 추출**: Trafilatura(블로그) + Jina Reader API(JS 사이트) + FxTwitter(X/Twitter)
- **트렌드 수집**: [last30days](https://github.com/mvanhorn/last30days-skill) 오픈소스 Claude Code 스킬 — Reddit·X·YouTube·웹 4소스, 2-Phase 수집(Broad Query → Community Drill-down), engagement 기반 스코어링(≥70점 필터), URL 정규화·중복제거
- **태스크 매칭**: Notion 2-DB 아키텍처(스킬 입력DB + 주간미팅DB), Claude 기반 업무 연관성 분석
- **시각화**: Google Gemini 3 Pro (4패널 코믹 다이어그램 자동 생성 + 무료 이미지 호스팅)
- **안전 장치**: Circuit Breaker, Kill Switch, 감사 로그(JSONL)

**규모 지표**:
- **2,549 LOC** Python (autoskill ~2,005 + trend-bridge 544)
- **5-Stage 자율 파이프라인**: URL 폴링 → 콘텐츠 추출 → 스킬 생성 → 태스크 매칭 → 다이어그램 생성
- **3-Tier 콘텐츠 추출 폴백**: Trafilatura(일반) → Jina Reader(JS 사이트) → FxTwitter(X)
- **Notion 2-DB 아키텍처**: 스킬 입력 DB(6개 상태 워크플로우) + 주간 미팅 DB(태스크 매칭 레퍼런스)
- **생성된 스킬 예시**: ai-agent-orchestrator, claudeception(자기참조 스킬 생성기), web-slide-creator 등
- 데몬 모드: `--daemon`(5분 간격 자동 실행), `--interval N`(커스텀), `--dry-run`(프리뷰)

#### "트렌디한 기술을 빠르게 내재화하는" 3단계 구조

| 단계 | 구성 요소 | 역할 |
|:----:|----------|------|
| **1. 트렌드 감지** | last30days (오픈소스 스킬) | Reddit·X·YouTube·웹에서 최근 30일 트렌드를 2-Phase로 수집, engagement 기반 스코어링 |
| **2. 필터링·적재** | trend-bridge (커스텀) | 스코어 ≥70 필터, URL 정규화·중복제거, Notion DB 자동 생성 |
| **3. 스킬 생성** | autoskill (커스텀) | 콘텐츠 추출 → Claude Code headless 스킬 생성 → 태스크 매칭 → 시각화 |

> **Anthropic 연결**: Claude Code Skills 생태계의 오픈소스 스킬을 발견하고, 자사 파이프라인에 통합하여, 새로운 기술 트렌드가 발견될 때마다 자동으로 팀 역량이 확장되는 구조.
> 이것이 "Claude Code를 개인 도구가 아닌 **조직 역량 확장 플랫폼**으로 쓴다"는 것의 실체입니다.

#### 1.2(수동) → 1.4(자율): Part 1의 진화 아크

| 구분 | 1.2 AX팀 Skills (수동) | 1.4 Autoskill (자율) |
|:----:|------------------------|---------------------|
| 트리거 | 팀원이 스킬 필요 인식 | 트렌드 URL 자동 감지 |
| 제작 | 사람이 SKILL.md 작성 | Claude Code가 headless로 자율 생성 |
| 배포 | GitHub push → team sync | Notion DB → 파이프라인 자동 처리 |
| 매칭 | 팀 미팅에서 구두 공유 | Claude가 주간미팅 DB와 자동 매칭 |
| 시각화 | 없음 | Gemini 4패널 코믹 자동 생성 |

#### 파이프라인 아키텍처

```
[last30days skill]                      [trend-bridge]                     [autoskill]
/last30days "AI tools"                  report.json 로드                    Notion DB 폴링
  → Reddit/X/YouTube/Web 2-Phase 수집     → 스코어 필터링 (≥70점)              → 콘텐츠 추출
  → engagement 스코어링                    → URL 정규화·중복제거                → Claude Code -p 스킬 생성
  → report.json 출력            →→→→      → Notion 페이지 생성     →→→→      → 주간미팅 태스크 매칭
                                          → 소스별 프리필 (X 자동)             → Gemini 4패널 다이어그램
```

#### 안전 장치: Responsible AI 운영

> Anthropic의 핵심 가치인 "안전한 AI"를 자율 파이프라인 운영에 직접 적용한 사례입니다.

| 메커니즘 | 작동 방식 | 목적 |
|----------|----------|------|
| **Circuit Breaker** | 5회 연속 실패 → 300초 자동 중단 | 폭주 방지 |
| **Kill Switch** | `EMERGENCY_STOP` 파일 생성 시 즉시 중단 | 긴급 정지 |
| **감사 로그** | `pipeline_audit.jsonl` — 타임스탬프, 타입, 비용 기록 | 운영 투명성 |
| **Max Turns** | Claude Code `--max-turns 10` | 무한 루프 방지 |

**JD 연결 분석**:

| 연결 대상 | 구체적 매핑 |
|-----------|------------|
| **공고문 — AI 열정** | Claude Code의 headless mode(`-p --output-format json`)를 프로덕션 파이프라인에 적용하고, 오픈소스 Claude Code Skills 생태계(last30days)를 발견·통합하여 자사 파이프라인의 입력 엔진으로 활용. **Claude Code의 제품 기능뿐 아니라 커뮤니티 생태계까지 탐구하는 사용자** |
| **공고문 — 기술 이해관계자 세일즈** | CTO에게 "Claude Code로 이런 자동화가 가능합니다"를 라이브 데모할 수 있는 시스템. subprocess 호출, JSON 파싱, Circuit Breaker까지 설명 가능한 기술적 깊이 |
| **공고문 — 전략적 비즈니스 어드바이저** | 스타트업 Founder에게 "AI가 스스로 역량을 확장하는 시스템"의 실물을 보여줄 수 있음. "수동 스킬(1.2) → 자율 스킬(1.4)"이라는 진화 경로가 곧 스타트업 AI 도입의 청사진 |
| **공고문 — 분석적 + 창의적 실행** | 멀티소스 트렌드 수집·스코어링·URL 중복제거(분석적) + Claude 자율 스킬 생성·4패널 코믹 시각화(창의적). 분석과 창의가 파이프라인의 각 스테이지에 교대로 배치 |
| **전략문서 — Anthropic 제품 이해** | Claude Code의 `-p` 플래그, `--output-format json`, `--allowedTools`, `--max-turns`를 실전에서 활용. Anthropic 제품의 "숨겨진 기능"까지 탐구하는 사용자 = AE가 고객에게 제품의 전체 스펙트럼을 설명할 수 있는 역량 |
| **이력서 — 얼리 어답터 DNA** | AI News Reporter(3.1)가 수동 모니터링의 자동화였다면, Autoskill은 **스킬 제작 자체의 자동화**. 도구 사용 → 오픈소스 스킬 생태계 활용 → 커스텀 브리지 구축 → 도구가 도구를 만듦. **기술 진화의 극단적 형태이자 Claude Code 에코시스템 참여의 증거** |

---

## Part 2: "F&F AI 전환" — 엔터프라이즈 AI 시스템

> 이 섹션은 "4000만원 PoC에서 10억 규모 전사 확장"이라는 이력서의 핵심 성과를 기술적으로 뒷받침합니다.
> 스타트업 고객이 Claude와 함께 걸어가야 할 여정을, 이미 고객 입장에서 걸어본 증거입니다.

---

### 2.1 FNF Studio — AI 패션 이미지 생성 MCP 서버 (Varco Art 대체 → 자체 플랫폼 내재화)

**한줄 설명**: NC소프트 Varco Art(외부 벤더) 의존에서 탈피, 17개 MCP 도구·12기준 품질검증·7,350 프리셋을 갖춘 자체 AI 이미지 생성 플랫폼으로 내재화 성공

**디렉토리**: `c:\python\venv\fnf-image-gen-mcp\`

**기술 스택**:
- **서버**: Python, FastMCP, SSE 원격접속 + stdio 듀얼 트랜스포트
- **이미지 생성**: Gemini 3 Pro Image API, 7단계 파이프라인 (프리셋→프롬프트→생성→검증→보정→저장→갤러리)
- **품질검증**: 12-Criterion MLBValidator (VLM 기반), Auto-Fail 게이트 11개
- **브랜드 인코딩**: Brand DNA 계층적 프롬프트 스키마 (착장→포즈→무드→배경)
- **데이터**: SQLite (프리셋 DB), API 키 자동 로테이션, 결과 CSV 내보내기

**규모 지표**:
- **119개** Python 파일, **17개** MCP 도구 (브랜드컷, 단일/멀티 Virtual Try-On, 배경교체, AI 인플루언서, 셀카/UGC, 갤러리, CSV 내보내기 등)
- **12-Criterion MLBValidator**: 가중치 체계 (photorealism 8%, anatomy 8%, face_identity 15%, outfit_accuracy 15%, color_accuracy 8%, composition 8%, lighting 8%, background 5%, brand_consistency 10%, commercial_viability 5%, detail_quality 5%, overall_impression 5%), S/A/B/C/F 등급, **11개 Auto-Fail 게이트** (얼굴 미생성, 손 기형, 로고 누락, 배경 불일치 등)
- **7,350개 프리셋 조합** (75 포즈 × 98 씬, 호환성 매트릭스 포함)
- **Brand DNA 인코딩**: 브랜드별 착장 스키마 → 포즈 프리셋 → 무드/배경 매핑, 온도 스케줄 워크플로우별 차등 (브랜드컷 0.25 vs 셀카 0.7)
- **AI 인플루언서 캐릭터 시스템**: 얼굴특징, 스타일선호도, 브랜드친화도를 JSON 프로파일로 관리
- SSE 기반 원격접속으로 팀원 다수 동시 사용, `python server.py` 한 줄 기동

#### 내재화 스토리: Varco Art → FNF Studio

> 이 스토리는 전략문서의 "4000만원 PoC를 10억으로 키운 사이클"의 구체적 기술 여정입니다.
> "외부 솔루션 의존 → 자체 플랫폼 구축"이라는 경로 자체가, AE가 스타트업 고객에게 "AI 내재화를 어떻게 하나"를 설명할 때 가장 생생한 사례입니다.

**Phase 1: 외부 벤더 의존 (NC소프트 Varco Art)**

- NC소프트 Varco Art로 AI 이미지 생성 시작
- 문제점: 높은 이미지당 비용(¥2,500+), 브랜드 DNA 인코딩 불가, 느린 이터레이션(벤더 커뮤니케이션 → 수정 요청 → 재생성), 품질검증 수동

**Phase 2: PoC (4,000만원) — 첫 자체 실험**

- Gemini로 단일 브랜드컷 생성 파이프라인 구축
- 6기준 품질검증 도입 (photorealism, anatomy, face, outfit, color, composition)
- 결과: "외부 벤더 없이도 된다"는 것을 증명 → 경영진 설득 근거 확보

**Phase 3: 플랫폼 통합 — 도구 확장 + 체계화**

- 6개 추가 도구 개발: Virtual Try-On, 배경교체, AI 인플루언서, 셀카/UGC 등
- 프리셋 DB 구축 (75 포즈 × 98 씬 = 7,350 조합), 호환성 매트릭스로 잘못된 조합 방지
- 품질검증 6기준 → **12기준 업그레이드**, Auto-Fail 게이트 11개 추가
- Brand DNA 인코딩: 브랜드별 착장 스키마를 코드로 체계화

**Phase 4: 전사 배포 — MCP 표준화 + 원격접속**

- SSE 기반 원격접속: 팀원이 `npx mcp-remote`로 어디서든 접속
- MCP 프로토콜 표준화: Claude Code에서 자연어 명령으로 이미지 생성
- API 키 자동 로테이션: 대량 생성 시 Rate Limit 자동 우회
- 연간 비용 절감 효과 극대화

**핵심 성과 수치**:

| 지표 | Varco Art (외부) | FNF Studio (자체) | 개선율 |
|------|:----------------:|:-----------------:|:------:|
| 이미지당 비용 | ¥2,500+ | ¥500-800 | **68-80% 절감** |
| 생성 속도 | 20-30초 | 10-15초 | **50% 단축** |
| 품질 통과율 (S/A 등급) | 수동 검수 | **78% (1차 시도)** | 자동화 |
| 프롬프트 엔지니어링 | 매번 수동 작성 | 프리셋 재사용 | **80% 절감** |
| 품질검증 기준 | 없음 (주관적) | 12기준 + 11 Auto-Fail | **정량화** |

**JD 연결 분석**:

| 연결 대상 | 구체적 매핑 |
|-----------|------------|
| **전략문서 — PoC를 전사로 키운 사이클** | Phase 1→4의 진화가 곧 "4000만 PoC → 10억 전사 확장"의 기술 여정. 이 4단계를 직접 설계·실행·검증한 경험은, 스타트업 고객에게 "AI 내재화의 로드맵"을 제시할 때 추상적 프레임워크가 아닌 실제 경험에서 나온 것 |
| **공고문 — B2B 세일즈** | 팀이 매일 사용하는 프로덕션 도구. "될 겁니다"가 아니라 "쓰고 있습니다"를 증명하는 시스템. 외부 벤더 대비 68-80% 비용 절감이라는 ROI를 직접 만들어본 경험 |
| **공고문 — 기술 이해관계자** | MCP 프로토콜, SSE 아키텍처, 12-Criterion 품질검증 파이프라인, Brand DNA 인코딩을 CTO에게 직접 설명할 수 있는 기술적 깊이. "이미지 생성 AI"를 아는 것이 아니라 "이미지 생성 AI의 품질을 어떻게 통제하는가"를 아는 것 |
| **이력서 — Varco Art 프로젝트** | NC소프트 Varco Art 솔루션 도입 PM → 한계를 직접 경험 → 자체 대안 구축 → 전사 배포. "외부 솔루션의 한계를 겪고, 내재화로 해결한" 완결된 스토리. AE가 고객에게 "벤더 의존 vs 자체 구축"을 조언할 때의 실전 데이터 |
| **공고문 — 분석적 + 창의적 실행** | 12기준 가중치 체계 + Auto-Fail 게이트 = 품질을 "느낌"이 아니라 "점수"로 관리하는 분석적 접근. 7,350 프리셋 조합 = 도메인 지식을 시스템으로 인코딩하는 창의적 접근 |

---

### 2.2 FNF Entertainment Insights Dashboard + Grok VLM 지식단절 극복

**한줄 설명**: 4개 플랫폼 실시간 트렌드 분석 대시보드 — AI 영상 분석 과정에서 VLM 지식 단절 문제를 Grok 하이브리드 파이프라인으로 해결

**디렉토리**: `c:\python\venv\fnf_enter\` (대시보드), `c:\python\venv\grok(all_about)\` (Grok 파이프라인)

**기술 스택**:
- **대시보드**: Next.js 15 (App Router + Turbopack), NestJS 11, TypeScript, pnpm + Turborepo 모노레포, Apify (웹 스크래핑), Recharts (시각화), Passport JWT (인증), Tailwind CSS 4, Radix UI
- **AI 분석 파이프라인**: Python, xAI Grok API (`grok-4-1-fast`), Google Gemini (`gemini-3-pro-preview`), PostgreSQL (DW 연동), 3-Tier 엔리치먼트 (Local KB → Cache → Grok API)

**규모 지표**:
- 4개 소셜 플랫폼 동시 수집·분석 (Instagram, TikTok, YouTube, X)
- UnifiedContent 포맷으로 플랫폼별 데이터 정규화
- Webhook 기반 실시간 업데이트
- 챌린지 대시보드 + 트렌드 현황 + AI 기반 영상 분석 리포트
- 5-Category 분석 프레임워크 (Identity, Performance, Visual, Engagement, Audio)

#### 문제해결 사례: VLM 지식 단절 극복

> 이 사례는 "AI가 작동하지 않을 때 어떻게 하는가"를 보여줍니다.
> 전략문서의 "Claude가 처음으로 작동했습니다"의 반대편 — **AI가 실패할 때 함께 해결하는 컨설턴트 역량**의 증거입니다.

**문제 정의**:

대시보드의 AI 영상 분석 기능은 Gemini Vision으로 K-pop 챌린지/밈 영상을 자동 분석합니다. 그런데 Gemini의 **지식 단절(Knowledge Cutoff: 2025년 1월)**이 치명적 문제를 일으켰습니다. 2025년 8월에 데뷔한 CORTIS(Big Hit Music), SM의 Hearts2Hearts 같은 최신 그룹을 **전혀 인식하지 못했습니다**. 소속사도, 멤버 이름도, 장르도 모두 "Unknown".

트렌드 분석 대시보드에서 최신 트렌드를 분석하지 못하면 — 그것은 대시보드가 아닙니다.

**해결 방법 — 2단계 하이브리드 파이프라인**:

```
[Stage 1] Grok 실시간 검색 (grok-4-1-fast)
  • 해시태그·음원·계정명으로 쿼리 생성
  • 웹 검색 (kprofiles, 나무위키, Wikipedia)
  • X(Twitter) 실시간 트렌드 검색
  • 소속사, 멤버, 데뷔일, 장르 추출
  • 소요: ~30-40초
          ↓
[Stage 2] 컨텍스트 주입 → Gemini 비전 분석
  • Grok 결과를 [K-pop Context]로 프롬프트에 주입
  • Gemini가 "이 영상에 나온 사람은 CORTIS의 Martin, James..."를 알고 분석
  • 5-Category 프레임워크로 구조화된 분석 결과 생성
  • 소요: ~40-50초
```

**3-Tier 엔리치먼트 전략** (비용 최적화):

| Tier | 소스 | 비용 | 용도 |
|------|------|------|------|
| 1 | Local KB (PostgreSQL crawl_targets) | $0 | 이미 아는 그룹 즉시 매칭 |
| 2 | File Cache (24h TTL) | $0 | 최근 조회한 그룹 재사용 |
| 3 | Grok API 호출 | ~$0.005 | 새로운/미지의 그룹만 검색 |

**A/B 테스트 결과** (공정한 비교를 위해 Gemini API 직접 호출):

| 그룹 | 지표 | Grok 있을 때 | Grok 없을 때 |
|------|------|:----------:|:----------:|
| **CORTIS** (2025.8 데뷔) | 소속사 식별 | Big Hit Music (HYBE) | ❌ Unknown |
| | 멤버 이름 | Martin, James, Juhoon... | ❌ Unknown |
| | 세대 분류 | 5세대 보이그룹 | ❌ Unknown |
| | **바이럴리티 점수** | **9/10** | **0/10** |
| **Hearts2Hearts** (SM) | 소속사 식별 | SM Entertainment | ❌ Unconfirmed |
| | 멤버 수 | 8명 | ❌ Unconfirmed |
| | 앨범/장르 | Mini 1st《FOCUS》/ Nu-Disco | ❌ Unconfirmed |
| | **바이럴리티 점수** | **9/10** | **0/10** |

> **핵심**: 바이럴리티 점수 **0 → 9**. 동일한 영상, 동일한 프롬프트, 유일한 차이는 Grok 컨텍스트 주입 여부.

**비용/성능**:
- 전체 파이프라인: ~$0.055/건, ~70-90초
- Grok 추가 비용: ~$0.005 (전체의 9%)
- 품질 개선: 0점 → 9점 (분석 불가 → 프로급 분석)

**JD 연결 분석**:

| 연결 대상 | 구체적 매핑 |
|-----------|------------|
| **전략문서 — 콘텐츠/미디어 세그먼트** | "CJ ENM에서 5.6년, 크리에이터와 미디어 스타트업이 AI에 어떻게 반응하는지 직접 겪었습니다" — 이 대시보드가 그 경험의 기술적 산출물 |
| **공고문 — 기술 이해관계자 세일즈** | AI 모델의 구조적 한계(지식 단절)를 정확히 진단하고, 다른 모델(Grok)로 보완하는 하이브리드 아키텍처 설계. CTO에게 "모델 한계와 우회 전략"을 A/B 테스트 데이터와 함께 설명할 수 있는 역량 |
| **공고문 — 분석적 + 창의적 실행** | 문제 진단(분석적) → 하이브리드 파이프라인 설계(창의적) → A/B 테스트 검증(분석적) → 3-Tier 비용 최적화(창의적). "분석과 창의의 반복 루프"를 실제로 돌린 증거 |
| **공고문 — 한국 시장** | K-pop 최신 트렌드를 실시간으로 추적해야 하는 한국 시장 특유의 요구사항. CORTIS, Hearts2Hearts 같은 최신 그룹을 놓치면 트렌드 분석의 의미가 없음 |
| **이력서 — 인플루언서 마케팅 통합 관리** | "인플루언서 마케팅 성과 추적 시간 70% 단축" 성과의 기술적 기반 |
| **전략문서 — AE의 컨설턴트 역할** | 스타트업 고객이 "Gemini/Claude로 하려는데 안 돼요"라고 할 때, "이렇게 우회하면 됩니다"를 직접 보여줄 수 있는 실전 경험. AE는 단순히 파는 사람이 아니라 기술적 실패를 함께 해결하는 파트너 |

---

### 2.3 인플루언서 시딩 콘텐츠 관리 플랫폼 (FnCo)

**한줄 설명**: 크롤링→AI기획→이미지생성→인플루언서분석→영상분석→성과추적까지 End-to-End 인플루언서 마케팅 플랫폼

**디렉토리**: `c:\python\venv\fnco_influencer_seeding-main\`

**기술 스택**:
- **Frontend**: React 18 + Vite 6, Redux Toolkit, Tailwind CSS v4 + shadcn/ui (40+ 컴포넌트), MUI X Data Grid Premium, Recharts, ReactFlow
- **Backend**: Express.js v5, PostgreSQL, Socket.IO (실시간), Multer (파일 업로드 500MB)
- **AI/ML**: FastAPI 마이크로서비스, Gemini AI (분석), Google Imagen (이미지 생성)
- **인프라**: Azure AD SSO (MSAL), AWS S3, RBAC 3단계 (read_all / read_team / read_self)
- **크롤러**: instaloader, yt-dlp, TikTokApi, tweepy, Playwright, gallery-dl

**규모 지표**:
- 3개 리전 지원 (한국 ko / 중국 cn / 글로벌 eng)
- 4단계 콘텐츠 라이프사이클 (Seeding → Preview → UGC → Performance)
- AI Plan: 마케팅 기획서(PDF/PPT) 업로드 → Gemini 분석 → 전략·시나리오 자동 생성
- AI 영상 분석: 훅 최적화, 스토리텔링, 플랫폼 최적화 등 8개 항목 개선 제안
- PDF/PPT 내보내기 자동화

**JD 연결 분석**:

| 연결 대상 | 구체적 매핑 |
|-----------|------------|
| **공고문 — B2B 세일즈** | Azure AD SSO + RBAC = 진짜 엔터프라이즈 수준 B2B SaaS. 스타트업이 이런 시스템을 만들고 싶어할 때 "제가 만들어봤습니다"를 말할 수 있는 증거 |
| **전략문서 — 한국 시장 전략** | 3개 리전(한국/중국/글로벌) 지원. 이력서의 "중국 법인 120명 AI 전환" 성과의 플랫폼 기반 |
| **공고문 — 전략적 비즈니스 어드바이저** | 마케팅 기획서 → AI 분석 → 콘텐츠 생성 → 성과 추적이라는 완전한 워크플로우. 스타트업 Founder에게 "AI를 비즈니스에 어떻게 녹이나"의 실제 사례 |
| **이력서 — F&CO 인플루언서 시딩** | "인플루언서 마케팅 성과 추적 시간 70% 단축, 의사결정 속도 50% 향상" 성과의 직접적 산출물 |

---

### 2.4 Content Factory — 뷰티 콘텐츠 Knowledge Graph + Graph RAG

**한줄 설명**: 194개 뷰티 영상의 인게이지먼트 데이터 + VLM 멀티모달 분석 → Neo4j Knowledge Graph → 4-Tool Graph RAG로 콘텐츠 기획서 자동 생성

**디렉토리**: `c:\python\venv\content_factory\`

**전략 테제 — "LLM + 데이터 = 스타트업 해자"**:

> 프론티어 LLM의 범용 역량이 올라갈수록, 스타트업의 차별화는 **자사 데이터를 LLM이 추론할 수 있는 지식 구조로 변환하는 능력**에 달립니다.
> 이 프로젝트는 "뷰티 콘텐츠 인게이지먼트 데이터"라는 원시 데이터를 Knowledge Graph로 구조화하고, Graph RAG로 그 위에서 LLM이 추론하게 만든 실물 증거입니다.

**기술 스택**:
- **Knowledge Graph**: Neo4j (v5 프로덕션), NetworkX (v1-v4 레거시)
- **Graph RAG**: neo4j-graphrag-python (`HybridRetriever` — 벡터검색 + 전문검색 동시 수행), Cypher 쿼리
- **LLM**: Google Gemini (Flash/Pro), Intent Router (LLM 기반 의도 분류 → 4개 도구 자동 라우팅)
- **VLM 분석**: Gemini 2.0 Flash (영상/이미지 속성 추출), Google Cloud Vision (라벨/객체/색상)
- **데이터 수집**: PRAW (Reddit), Playwright (TikTok), Instaloader + Apify (Instagram), pytube (YouTube)
- **자동화**: n8n 워크플로우 (매일 07:00 KST 자동 실행)

**규모 지표**:
- **5세대 진화**: v1(NetworkX 프로토타입) → v2(속성 확장) → v3(Hook 분류 체계) → v4(RAG 통합) → **v5(Neo4j 프로덕션, HybridRetriever)**
- **KG 노드 타입**: Video, Scene, Hook(12종), Camera(6종), Sound(5종), Visual(7종), Product(4종)
- **194개 실제 뷰티 영상** 분석 데이터, 씬 단위 멀티모달 분석 (타임스탬프별 시각/음향/훅/카메라 추출)
- **4-Tool 에이전틱 RAG** (LLM Intent Router가 사용자 질문을 분류 → 적합한 도구 자동 선택):
  1. `analyze_performance()` — 고성과 영상 패턴 분석 (Cypher: Top-N% 영상의 공통 속성 집계)
  2. `recommend_recipe()` — 키워드 기반 씬 추천 (HybridRetriever: 벡터+전문검색 동시 수행)
  3. `diagnose_hook()` — 훅 효과 진단 (Cypher: 고성과 vs 저성과 비교 분석)
  4. `generate_draft_plan()` — 3단계 콘텐츠 기획서 생성 (Draft 초안 → 씬 매칭 → HTML 스토리보드)
- **Hook 12종 분류 체계**: Fame, Visual Shock, ASMR/Sensory, Story, Result, Emotional, Contradiction, Utility, Cultural, Pain, Myth, Trend
- 출력: HTML 스토리보드, 랭킹 플랜, 인터랙티브 그래프 시각화

#### 5세대 진화: NetworkX → Neo4j

| 세대 | 핵심 변경 | 한계 → 다음 세대로 |
|:----:|-----------|-------------------|
| v1 | NetworkX 그래프 프로토타입, JSON→Graph 변환 | 검색 속도 한계, 임베딩 미지원 |
| v2 | 속성 노드 확장 (Camera 6종, Sound 5종, Visual 7종, Product 4종) | Hook 분류 미정형 |
| v3 | Hook 12종 표준 분류 체계 도입 + 유의어 사전 | RAG 미연동 |
| v4 | RAG Orchestrator 통합, 4-Tool Intent Router | 그래프 DB 확장성 한계 |
| **v5** | **Neo4j 마이그레이션**, HybridRetriever (벡터+전문검색), Cypher 쿼리 최적화 | **현재 프로덕션** |

**JD 연결 분석**:

| 연결 대상 | 구체적 매핑 |
|-----------|------------|
| **공고문 — 기술 이해관계자 세일즈** | CTO에게 "당신의 데이터를 KG로 구조화하면 Claude가 이렇게 추론합니다"를 Neo4j + Cypher 쿼리 + 4-Tool RAG라는 실물로 설명 가능. "데이터 + LLM = 해자"를 추상적 슬라이드가 아니라 동작하는 코드로 보여줄 수 있는 역량 |
| **공고문 — 전략적 비즈니스 어드바이저** | 스타트업 Founder에게 "AI를 어떻게 비즈니스에 녹이나"의 가장 구체적인 답: ① 데이터 수집 → ② 지식 구조화(KG) → ③ LLM 추론(RAG) → ④ 비즈니스 산출물(기획서). 이 4단계를 직접 설계·구축·5세대까지 반복 개선한 경험 |
| **공고문 — 분석적 + 창의적 실행** | Cypher 쿼리로 "왜 이 영상이 잘 되는가"를 정량 진단(분석적) + 12종 Hook 분류 체계와 Graph RAG로 기획서 자동 생성(창의적). `diagnose_hook()`의 고성과/저성과 비교 분석은 A/B 테스트와 같은 사고방식 |
| **전략문서 — 패션/이커머스 + 콘텐츠/미디어** | 두 세그먼트의 교차점(뷰티 콘텐츠)에서 실제 프로덕트를 만든 경험. "K-beauty + 소셜 콘텐츠"는 한국 스타트업 생태계의 핵심 버티컬 |
| **이력서 — RAG 챗봇 → KG RAG** | "사내 지식 문서 RAG 챗봇(정보 검색 80% 단축)"의 진화형. RAG → Graph RAG로의 기술 업그레이드를 직접 수행한 궤적 |
| **공고문 — AI 열정** | NetworkX→Neo4j 5세대 진화 = "새 기술이 나오면 직접 마이그레이션하는 사람". Graph RAG는 2024년 주류화된 기술인데, 그걸 실제 프로덕션 데이터에 적용해본 경험 |

---

### 2.5 전사 AI 교육 & AI Committee 운영 — "도구에서 사람으로"

**한줄 설명**: F&F 전사 320명 AI 전환 교육 기획/운영 + AI Committee(AI 협의체) 메인 PM + CEO/CDO 정기 기술 브리핑 — 코드 프로젝트가 아닌 **"조직 변혁"** 경험

**소스**: PDF 포트폴리오 Pages 35-39, 이력서, 전략문서 (코드베이스가 아닌 Notion 기반 운영 자료)

> Part 2의 4개 프로젝트(2.1~2.4)는 "AI 도구"를 만든 이야기입니다.
> 이 섹션은 **"AI 도구를 쓰는 사람"을 만든 이야기**입니다.
> 도구를 만드는 것과, 그 도구를 320명이 매일 쓰게 만드는 것은 완전히 다른 역량입니다.
> 그리고 이 내부 경험이 외부 스타트업 C-Level 교육(전략문서의 Context Architect Training)으로 이어졌고,
> 궁극적으로 **Anthropic AE라는 역할 — "Claude를 조직에 도입하도록 돕는 사람"**으로 귀결됩니다.

**핵심 프로그램** (4가지):

**① AI Committee (AI 협의체) — 메인 PM**
- 사내 AX 육성 프로그램, **메인 PM**으로 운영
- CEO(회장) / CDO(상무이사·본부장) **정기/비정기 보고** 담당
- AI 기술 동향 리서치 → C-Level 보고 자료 작성
- 2026 신년회: **전사 마케팅 AX 로드맵** 발표

**② 전사 AI 교육 (국내) — 200명+**
- LLM 활용 교육 **200명+** 직접 기획 및 강의
- 커리큘럼 구성: 패션 디자이너, 콘텐츠 크리에이터, 마케터, E-Biz 등 **직군별 맞춤**
- 교육 → 스킬 제작(1.2) → 팀 공유 → 재교육의 **선순환 구조** 설계

**③ 중국 법인 AI 전환 — 120명**
- 120명 대상 AI 교육 실행 (LLM 활용 기초 + 업무 자동화 Agent)
- 만족도 **4.8/5.0** 달성
- 크로스보더 프로젝트: 한국↔중국 간 AI 워크플로우 표준화

**④ AI Challengers 프로그램**
- 핵심 인재 선발 및 집중 육성
- 성과: 핵심 인재 선정 및 **특진** (하반기 승진)

**규모 지표**:
- **한국 200명 + 중국 120명** = **320명** AI 네이티브 전환
- CEO(회장) / CDO(상무이사) **정기 보고**
- 중국 법인 교육 만족도 **4.8/5.0**
- 전사 마케팅 AX 로드맵 설계 및 신년회 발표
- 핵심 인재 특진: 교육→성과→승진 루프 입증

#### 내러티브: "내부에서 외부로"

```
[내부] F&F 200명 AI 교육 (직군별 맞춤 커리큘럼)
        ↓
[내부] 중국 법인 120명 AI 전환 (크로스보더)
        ↓
[외부] 스타트업 C-Level 교육 (더플레이컴퍼니 16명, 유니브 CEO 8강)
        ↓
[목표] Anthropic AE — "Claude를 조직에 도입하도록 돕는 사람"
```

> AE가 스타트업 고객에게 "Claude를 조직에 어떻게 도입하나?"라고 물을 때,
> 실제 320명 규모 AI 전환을 리딩한 PM이 답하는 것과 "이론적으로 이렇습니다"는 차원이 다릅니다.

**JD 연결 분석**:

| 연결 대상 | 구체적 매핑 |
|-----------|------------|
| **공고문 — 전략적 비즈니스 어드바이저** | 스타트업 Founder가 "AI를 우리 조직에 어떻게 도입하지?"라고 물을 때, "F&F에서 320명을 이렇게 전환했습니다"를 답할 수 있는 유일한 AE 후보. 교육 커리큘럼 설계 → 실행 → 만족도 4.8의 전 과정을 직접 리딩한 경험 |
| **공고문 — B2B 세일즈** | AI 도입은 기술 구매가 아니라 조직 변혁. "Claude를 샀으니 끝"이 아니라 "교육 → 스킬 제작 → 팀 공유 → 재교육"이라는 **도입 사이클**을 직접 설계하고 320명에게 적용한 경험. 이것이 Enterprise Sales의 본질 |
| **공고문 — 기술 이해관계자 세일즈** | CEO(회장)과 CDO(상무이사)에게 AI 기술 동향을 정기 보고한 경험 = **비기술자 C-Level에게 기술을 설명하는 역량**. AE가 CTO뿐 아니라 CEO에게도 Claude의 가치를 설명해야 할 때의 실전 경험 |
| **전략문서 — "내부에서 외부로"** | F&F 내부 320명 교육 → 더플레이컴퍼니/유니브 스타트업 C-Level 30명+ 교육 → Anthropic AE(전체 한국 스타트업). "가르치는 사람"에서 "도입을 돕는 사람"으로의 자연스러운 확장 |
| **이력서 — AI 교육 실적** | "전사 LLM 특강 한국 150명, 중국 120명", "AI Committee 운영", "Context Architect Training" — 이 세 줄의 이력서 텍스트 뒤에 있는 실제 경험의 깊이와 맥락 |
| **공고문 — 한국 시장** | 한국 200명 + 중국 120명의 **다지역 교육 경험**. 한국 시장의 패션/이커머스 조직 문화와 AI 수용도를 내부자로 경험. 중국 법인 교육은 크로스보더 확장 역량의 증거 |

---

## Part 3: "스타트업 생태계에 전하겠습니다" — AI 생태계 리터러시 + 기술적 깊이

> 이 섹션은 "왜 이 사람이 다른 AE 후보보다 나은가"를 증명합니다.
> AI 산업 전체를 시스템적으로 추적하는 습관(3.1)과, 엔지니어와 동등하게 대화할 수 있는 기술적 깊이(3.2)입니다.

---

### 3.1 AI News Reporter Agent

**한줄 설명**: Anthropic Blog 등 주요 AI 소스를 자동 수집·분석하고, LLM 가격 비교표를 생성하는 뉴스 에이전트

**디렉토리**: `c:\python\venv\ai_news_reporter\`

**기술 스택**: Python, Google Gemini API, Playwright (헤드리스 브라우저), Notion API, CLI

**규모 지표**:
- 6개 글로벌/한국 소스 자동 추적 (TechCrunch AI, **Anthropic Blog**, OpenAI Blog, AI Times, ZDNet Korea, generic)
- 뉴스 분석 + API 문서 분석 + 가격 비교 계산기 3가지 모드
- Notion DB 자동 동기화로 주간 리포트 생성
- 크롤러 → 분석기 → 리포터 3계층 아키텍처

**JD 연결 분석**:

| 연결 대상 | 구체적 매핑 |
|-----------|------------|
| **공고문 — AI 열정, 특히 안전한 AI** | Anthropic Blog를 **1순위 크롤링 소스**로 설정. 경쟁사 블로그가 아니라 Anthropic의 안전한 AI 연구를 가장 먼저 추적한다는 것 자체가 지원 동기의 증거 |
| **전략문서 — 시장 기회 포착** | LLM 가격/성능 비교 계산기 = AE가 고객에게 "왜 Claude인가?"를 설명할 때 필요한 핵심 데이터. 이미 시스템화해서 운영 중 |
| **공고문 — 분석적 실행** | 경쟁사 동향을 "가끔 읽는다"가 아니라 자동화 시스템으로 만든 습관. 분석적 접근의 극단적 형태 |
| **이력서 — 얼리 어답터 DNA** | "영문 Technical Paper 실시간 모니터링 및 비즈니스 적용"이라는 역량의 기술적 증거 |

---

### 3.2 Linn Custom Nodes — AI 패션 촬영 자동화 (ComfyUI)

**한줄 설명**: 28,820줄 Python, 104+ 커스텀 노드로 구성된 AI 비디오/이미지 생성 파이프라인 (ComfyUI 프레임워크)

**디렉토리**: `D:\comfy\custom_nodes\Linn_node\`

**기술 스택**: Python (28,820 LOC), ComfyUI, Google Gemini AI (2.5 Flash / 3.0 Pro), Kling AI (Video Generation), ElevenLabs (TTS), YouTube API, OpenCV, Pillow, NumPy

**규모 지표**:
- **28,820줄** Python 코드, **53개** Python 모듈, **104+** ComfyUI 커스텀 노드
- Photography DNA 시스템 3종 (Studio / Outdoor / Snapshot — 카메라, 렌즈, 조명, 분위기까지 세밀한 프롬프트 엔지니어링)
- 비디오 분석 파이프라인: 영상 로드 → AI 분석(Gemini) → JSON 샷 플랜 → 샷 분리 → 프레임 추출 → 이미지 생성 → 비디오 합성
- 배치 처리: CAD 일러스트 → 실사 스튜디오 포토 대량 변환
- 페이스 스왑, 배경 합성(3버전), 포즈 변형, 텍스처 변형, 컬러/무드 조정
- 메모리 시스템: 세션 기반 + 파일 기반 영속 저장 (비용 최적화)

**JD 연결 분석**:

| 연결 대상 | 구체적 매핑 |
|-----------|------------|
| **공고문 — 기술 이해관계자 세일즈** | 28K LOC는 "비개발자가 LLM과 협업해서 코드를 쓴다"의 극단적 증거. 스타트업 CTO와 동등한 수준에서 기술 대화가 가능하다는 증명 |
| **전략문서 — "15만 이미지 자동화"** | 이 시스템이 대규모 이미지 처리 경험의 기술적 백본. 배치 처리, 품질 검증, 비용 최적화(메모리 시스템)까지 포함 |
| **공고문 — 혁신적 세일즈 전략** | Photography DNA 시스템 = 도메인 전문지식(패션 촬영)을 AI 프롬프트로 인코딩하는 방법론. 스타트업 고객에게 "도메인을 AI에 녹이는 법"을 가르칠 때의 최고의 사례 |
| **이력서 — 멀티모달 AI 전문성** | 텍스트(프롬프트) → 이미지(Gemini) → 비디오(Kling) → 오디오(ElevenLabs)까지 전 모달리티를 하나의 시스템에서 오케스트레이션 |

---

## 요약 매트릭스: 프로젝트 × JD 요건

| 프로젝트 | B2B세일즈 | 기술세일즈 | 전략어드바이저 | AI열정 | 분석실행 | 한국시장 |
|----------|:---------:|:---------:|:-------------:|:------:|:--------:|:--------:|
| **1.1** 이미지 태깅 자동화 | ★★★ | ★★ | ★★ | ★★★ | ★★★ | ★★★ |
| **1.2** AX팀 Skills | - | ★★★ | ★★ | ★★★ | ★ | ★★ |
| **1.3** KG MCP 서버 | ★★ | ★★★ | ★★★ | ★★ | ★★ | ★★★ |
| **1.4** Autoskill 자율 스킬 생성 | ★ | ★★★ | ★★ | ★★★ | ★★★ | ★ |
| **2.1** FNF Studio MCP | ★★★ | ★★★ | ★★★ | ★★ | ★★★ | ★★ |
| **2.2** Entertainment Dashboard + Grok | ★★ | ★★★ | ★★ | ★★ | ★★★ | ★★★ |
| **2.3** 인플루언서 시딩 | ★★★ | ★★ | ★★★ | ★ | ★★ | ★★★ |
| **2.4** Content Factory KG+RAG | ★★ | ★★★ | ★★★ | ★★★ | ★★★ | ★★★ |
| **2.5** 전사 AI 교육 & AI Committee | ★★★ | ★★ | ★★★ | ★★★ | ★★ | ★★★ |
| **3.1** AI News Reporter | ★ | ★ | ★★ | ★★★ | ★★★ | ★★ |
| **3.2** Linn Nodes | ★ | ★★★ | ★ | ★★ | ★★ | ★★ |
| **커버리지** | 7/11 | 10/11 | 9/11 | 11/11 | 10/11 | 9/11 |

> ★★★ = 핵심 증거, ★★ = 강한 연관, ★ = 간접 연관

**주목할 점**: "AI 열정" 요건은 **11개 프로젝트 전부**에서 커버됩니다. 이것이 "영업은 잘 하지만 AI를 직접 써본 경험이 없는 후보"와의 결정적 차이입니다. 특히 1.4 Autoskill은 Claude Code의 headless mode를 프로덕션 파이프라인에 적용한 **"Claude의 가장 깊은 곳까지 써본 증거"**이며, 2.5 전사 AI 교육은 **"320명 조직 변혁"**으로 AE의 핵심 역할인 "Claude 조직 도입 컨설팅"을 이미 수행한 증거입니다.

---

## 부록: 제외된 프로젝트 및 사유

| 프로젝트 | 디렉토리 | 제외 사유 |
|----------|----------|----------|
| video_planning_system | `c:\python\venv\video_planning_system\` | fnf_enter, Linn_node와 기능 중복 |
| data_integrity_agent | `c:\python\venv\data_integrity_agent\` | 내부 QA 도구. AE 스토리로 변환하기 어려움 |
| Stock (투자 에이전트) | `c:\python\venv\Stock\` | LangChain 기반, Claude 중심 아님. 패션/콘텐츠 버티컬과 무관 |
| career_portfolio_agent | `c:\python\venv\career_portfolio_agent\` | 자기참조적 — 지원서에 "지원서 만드는 도구"를 넣는 것은 순환 논리 |
| RAG/ | `c:\python\venv\RAG\` | 여러 조각 구현이 혼재. 단일 완성 스토리가 없음 (KG 시스템에 흡수) |
| ViMax | `D:\python_sub_for_video\ViMax\` | HKUDS 오픈소스 포크. 원본 저작 주장 불가 |
| beauty_reels_agent | `c:\python\venv\beauty_reels_agent\` | fnf-image-gen-mcp과 기능 중복 |
| sns_mood_background | `c:\python\venv\sns_mood_background\` | 이미지 생성 프로젝트들과 중복, 규모 작음 |
| Qwen3_api | `c:\python\venv\Qwen3_api\` | API 테스트 코드. 프로젝트라 부르기 어려움 |
| great-journey-ai-demo | `c:\python\venv\great-journey-ai-demo\` | 데모/프로토타입 수준, 깊이 부족 |

---

## 이 문서의 활용법

1. **면접 준비**: 각 프로젝트의 "JD 연결 분석" 테이블을 면접 답변의 골격으로 활용
2. **포트폴리오 첨부**: 이 문서 자체를 지원서 보조 자료로 제출 가능 (디렉토리 경로 → GitHub 링크로 교체 시)
3. **데모 준비**: Part 1의 세 프로젝트(Skills, KG, **Autoskill**)와 Part 2의 Content Factory는 Claude Code에서 실시간 시연 가능. 특히 Autoskill은 `claude -p` headless 모드의 라이브 데모로 최적
4. **스토리텔링**: Part 1→2→3 순서가 곧 "Claude 발견 → 전사 도입 → 생태계 확산"이라는 커리어 내러티브
5. **전략 테제 활용**: 2.4 Content Factory의 "LLM + 데이터 = 해자" 테제를 면접에서 "스타트업이 AI로 어떻게 차별화하나?"에 대한 답변 골격으로 활용
6. **교육 경험 면접 활용**: "Claude를 조직에 어떻게 도입하나?"라는 질문에 2.5의 320명 전환 경험(커리큘럼 설계→실행→만족도 4.8→특진)을 4단계 도입 사이클로 설명. 특히 "내부 320명 → 외부 스타트업 → Anthropic AE"의 확장 내러티브는 지원 동기의 핵심

---

*탐색 범위: 4개 디렉토리, 26개+ 프로젝트 전수 탐색*
*선정 기준: JD 6개 핵심 요건 × 전략문서 스토리 아크 (코드 10개 + 조직 경험 1개)*
*작성일: 2026-02-27*
