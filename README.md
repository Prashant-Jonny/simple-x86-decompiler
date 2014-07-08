#simple-x86-decompiler

simple x86 decompiler (for studying)

##Todo
  1. 구조 재설계
  1. 라이브러리 버그 해결
  1. 변수 타입 생략 금지
  1. 스텍 명칭을 시작점_끝점 으로 재정의
  1. 명칭 변경 asm LLIR MLIR HLIR C
  1. 위 단계에 따라 하는일을 확실하게 나눔
  1. 추가적인 디버그 정보가 있는경우 이용

##코드 구조
1. ELF 파일 파싱(elf_reader.py)
  1. 프로그램 시작점 찾기
  1. .dynamic, .dynstr, .dynsym, .plt 를 파싱해서 임포트, 익스포트 함수 리스트 생성
    1. .dynsym 에서 임포트 익스포트 함수 리스트를 생성
    1. .dynstr 에서 함수의 이름을 가져옴
    1. .plt 에서 함수 호출시 사용하는 주소를 가져옴
  1. 
1. 어셈블리어를 LLIR(low-level IR) 로 변환
  1. ?
1. LLIR을 MLIR(middle-level IR) 로 변환
  1. ?
1. MLIR을 HLIR(high-level IR) 로 변환
  1. ?
1. HLIR 을 C언어로 변환
