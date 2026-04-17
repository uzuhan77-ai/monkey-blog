from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from ..services.ai_service import AIConfigError, AIServiceError, generate_writing_assistant_result

class AIWritingAssistantView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self,request):
        topic = (request.data.get("topic") or '').strip()
        current_title = (request.data.get('current_title') or '').strip()
        current_summary = (request.data.get('current_summary') or '').strip()
        current_content = (request.data.get('current_content') or '').strip()

        if not any([topic, current_title,current_summary, current_content]):
            return Response(
                {"code": 400, "message": "请输入主题，或提供现有草稿内容。"},
                status=400,
            )
        keywords = request.data.get('keywords',[])
        if isinstance(keywords, str):
            keywords = [item.strip() for item in keywords.split(",") if item.strip()]
        elif isinstance(keywords, list):
            keywords = [str(item).strip() for item in keywords if str(item).strip()]
        else:
            keywords = []

        try:
            result = generate_writing_assistant_result(
                {
                    "topic": topic,
                    "keywords": keywords,
                    "audience": (request.data.get("audience") or "").strip(),
                    "tone": (request.data.get("tone") or "").strip(),
                    "current_title": current_title,
                    "current_summary": current_summary,
                    "current_content": current_content,
                }
            )

        except AIConfigError as exc:
            return Response({"code": 503, "message": str(exc)}, status=503)
        except AIServiceError as exc:
            return Response({"code": 502, "message": str(exc)}, status=502)

        return Response({"code": 200, "message": "AI 建议生成成功", "data": result})


