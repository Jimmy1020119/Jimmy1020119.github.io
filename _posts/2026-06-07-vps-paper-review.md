---
title: "[Review] Video Parallel Scaling (VPS): How to Give VideoLLMs More Eyes Without Blowing Up Your Memory"
date: 2026-06-07
categories: [Paper Review]
tags: [VideoLLM, VPS, Inference, Scaling, 논문, 리뷰]
description: "Video Parallel Scaling (VPS) — giving VideoLLMs more eyes without blowing up memory."
---

<div class="slides-wrapper" style="position:relative;width:100%;padding-top:57.76%;margin:2rem 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.18);">
  <iframe
    src="https://docs.google.com/presentation/d/e/2PACX-1vQXchIJaM1i8bFee7Un87Z5uTrBYJhYtwtH-GCm4XDmjm3rkTLKb8au4YVVoeD8HnXzr7ZuAG1noi-l/pubembed?start=false&loop=false&delayms=3000"
    style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
    frameborder="0"
    allowfullscreen="true"
    mozallowfullscreen="true"
    webkitallowfullscreen="true">
  </iframe>
</div>

## 한 줄 요약

**Video Parallel Scaling (VPS)** 는 VideoLLM이 더 많은 프레임("더 많은 눈")을 보면서도 메모리/연산 비용이 폭발하지 않도록, 비디오 입력을 **병렬로 나눠 처리**하는 추론 기법이다.

## 문제 의식

- VideoLLM은 입력 프레임 수가 늘수록 성능이 좋아지지만, 프레임이 많아지면 **토큰 수가 급증**해 KV 캐시·메모리·연산량이 함께 폭발한다.
- 그렇다고 프레임을 적게 넣으면 긴 영상에서 중요한 장면을 놓친다.
- 즉, **"더 많이 보기" vs "메모리 한계"** 사이의 트레이드오프가 핵심 병목이다.

## 핵심 아이디어

- 영상을 **여러 갈래(parallel stream)로 분할**해 각 스트림이 일부 프레임만 담당하게 한다.
- 각 스트림을 **병렬로 처리한 뒤 결과를 통합(aggregation)** 하여, 전체 프레임을 한꺼번에 한 컨텍스트에 넣지 않고도 넓은 시간 범위를 커버한다.
- 덕분에 **컨텍스트 길이를 선형으로 늘리지 않고도** 실질적으로 더 많은 프레임을 "본" 효과를 낸다 → 메모리 증가를 억제.

## 왜 효과적인가

- 긴 컨텍스트를 그대로 키우는 방식은 메모리가 제곱/선형으로 커지지만, VPS는 **병렬 분할 + 통합** 구조라 비용 증가가 완만하다.
- 추가 학습 없이 **추론 단계(inference-time scaling)** 에서 적용 가능한 점이 장점.

## 한 줄 정리

> 프레임을 더 보고 싶지만 메모리가 부족할 때, **"길게"가 아니라 "넓게(병렬로)"** 처리해서 VideoLLM에게 더 많은 눈을 달아주는 방법.

---

*위 요약은 매우 간소화한 설명입니다. 구체적인 수식·벤치마크 수치는 슬라이드를 참고하세요.*
