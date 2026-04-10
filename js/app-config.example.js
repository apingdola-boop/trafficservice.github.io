/**
 * ROUTE CALC — API·외부 서비스 설정 예시
 *
 * 사용법: 이 파일을 복사해 app-config.js 로 저장한 뒤 값을 채웁니다.
 *   (Windows) copy js\app-config.example.js js\app-config.js
 *
 * 공개 저장소: app-config.js 는 커밋하지 않고, 배포 파이프라인에서만 생성하는 것을 권장합니다.
 * (현재 Pages는 정적 파일이므로, 비공개 레포 또는 키 회전·카카오/Supabase 콘솔 제한으로 보완하세요.)
 */
window.RouteCalcConfig = {
    supabaseUrl: '',
    supabaseAnonKey: '',
    kakaoRestApiKey: '',
    /** EmailJS 대시보드의 public key (구 init에 쓰이던 값) */
    emailJsPublicKey: '',
};
