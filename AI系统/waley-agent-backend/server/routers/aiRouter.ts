import { z } from "zod";
import { router, protectedProcedure } from "../_core/trpc";
import { invokeLLM } from "../_core/llm";
import { invokeHermes } from "../_core/hermes";
import { buildDiagnosisContext, formatContextForLLM } from "../services/ragService";
import { saveChatMessage, getChatHistory } from "../db";
import { nanoid } from "nanoid";
import { ENV } from "../_core/env";

export const aiRouter = router({
  /**
   * 启动诊断会话
   */
  startDiagnosisSession: protectedProcedure
    .input(z.object({
      deviceId: z.number().optional()
    }))
    .mutation(async ({ ctx, input }) => {
      const sessionId = `SESSION-${nanoid(12)}`;
      
      // 保存会话开始消息
      await saveChatMessage({
        sessionId,
        deviceId: input.deviceId,
        userId: ctx.user.id,
        role: 'assistant',
        content: '您好！我是 Waley 智能运维助手。请描述您遇到的设备问题，我将为您提供诊断和解决方案。',
        metadata: JSON.stringify({ type: 'session_start' })
      });

      return { sessionId };
    }),

  /**
   * 获取 AI 诊断
   */
  getDiagnosis: protectedProcedure
    .input(z.object({
      sessionId: z.string(),
      deviceId: z.number(),
      message: z.string()
    }))
    .mutation(async ({ ctx, input }) => {
      // 保存用户消息
      await saveChatMessage({
        sessionId: input.sessionId,
        deviceId: input.deviceId,
        userId: ctx.user.id,
        role: 'user',
        content: input.message
      });

      // 构建诊断上下文
      const context = await buildDiagnosisContext(input.deviceId, input.message);

      // 格式化为 LLM 提示词
      const prompt = formatContextForLLM(context, input.message);

      // 确定使用哪个 AI 后端
      const useHermes = ENV.hermesApiUrl || true; // 默认启用 Hermes

      let assistantMessage: string;

      if (useHermes) {
        // 调用 Hermes
        try {
          const response = await invokeHermes({
            messages: [
              { role: 'system', content: '你是 Waley 工业设备智能运维助手，专门帮助用户诊断和解决工业设备故障。请用专业但易懂的语言回答问题。' },
              { role: 'user', content: prompt }
            ]
          });
          const messageContent = response.choices[0]?.message?.content;
          assistantMessage = typeof messageContent === 'string' ? messageContent : '抱歉，我暂时无法处理您的请求。';
        } catch (hermesErr) {
          console.error('[AI] Hermes failed, falling back to LLM:', hermesErr);
          // Fallback to direct LLM
          const response = await invokeLLM({
            messages: [
              { role: 'system', content: '你是 Waley 工业设备智能运维助手，专门帮助用户诊断和解决工业设备故障。请用专业但易懂的语言回答问题。' },
              { role: 'user', content: prompt }
            ]
          });
          const messageContent = response.choices[0]?.message?.content;
          assistantMessage = typeof messageContent === 'string' ? messageContent : '抱歉，我暂时无法处理您的请求。';
        }
      } else {
        // 直接调用 LLM
        const response = await invokeLLM({
          messages: [
            { role: 'system', content: '你是 Waley 工业设备智能运维助手，专门帮助用户诊断和解决工业设备故障。请用专业但易懂的语言回答问题。' },
            { role: 'user', content: prompt }
          ]
        });
        const messageContent = response.choices[0]?.message?.content;
        assistantMessage = typeof messageContent === 'string' ? messageContent : '抱歉，我暂时无法处理您的请求。';
      }

      // 保存助手回复
      await saveChatMessage({
        sessionId: input.sessionId,
        deviceId: input.deviceId,
        userId: ctx.user.id,
        role: 'assistant',
        content: assistantMessage,
        metadata: JSON.stringify({
          context: {
            hasDevice: !!context.device,
            alertCount: context.activeAlerts.length,
            workOrderCount: context.relatedWorkOrders.length
          }
        })
      });

      return {
        message: assistantMessage,
        context: {
          device: context.device,
          activeAlerts: context.activeAlerts.length,
          relatedWorkOrders: context.relatedWorkOrders.length
        }
      };
    }),

  /**
   * 获取对话历史
   */
  getChatHistory: protectedProcedure
    .input(z.object({
      sessionId: z.string()
    }))
    .query(async ({ input }) => {
      const history = await getChatHistory(input.sessionId);
      return history;
    }),

  /**
   * 快速诊断（无需会话）
   */
  quickDiagnosis: protectedProcedure
    .input(z.object({
      deviceId: z.number(),
      faultDescription: z.string()
    }))
    .mutation(async ({ input }) => {
      // 构建诊断上下文
      const context = await buildDiagnosisContext(input.deviceId, input.faultDescription);

      // 格式化为 LLM 提示词
      const prompt = formatContextForLLM(context, input.faultDescription);

      // 确定使用哪个 AI 后端
      const useHermes = ENV.hermesApiUrl || true;

      let diagnosis: string;

      if (useHermes) {
        // 调用 Hermes
        try {
          const response = await invokeHermes({
            messages: [
              { role: 'system', content: '你是 Waley 工业设备智能运维助手。请根据提供的设备信息和故障描述，给出简洁明了的诊断结果和解决方案。' },
              { role: 'user', content: prompt }
            ]
          });
          const diagnosisContent = response.choices[0]?.message?.content;
          diagnosis = typeof diagnosisContent === 'string' ? diagnosisContent : '抱歉，我暂时无法处理您的请求。';
        } catch (hermesErr) {
          console.error('[AI] Hermes failed, falling back to LLM:', hermesErr);
          // Fallback to direct LLM
          const response = await invokeLLM({
            messages: [
              { role: 'system', content: '你是 Waley 工业设备智能运维助手。请根据提供的设备信息和故障描述，给出简洁明了的诊断结果和解决方案。' },
              { role: 'user', content: prompt }
            ]
          });
          const diagnosisContent = response.choices[0]?.message?.content;
          diagnosis = typeof diagnosisContent === 'string' ? diagnosisContent : '抱歉，我暂时无法处理您的请求。';
        }
      } else {
        // 直接调用 LLM
        const response = await invokeLLM({
          messages: [
            { role: 'system', content: '你是 Waley 工业设备智能运维助手。请根据提供的设备信息和故障描述，给出简洁明了的诊断结果和解决方案。' },
            { role: 'user', content: prompt }
          ]
        });
        const diagnosisContent = response.choices[0]?.message?.content;
        diagnosis = typeof diagnosisContent === 'string' ? diagnosisContent : '抱歉，我暂时无法处理您的请求。';
      }

      return {
        diagnosis,
        context: {
          device: context.device,
          activeAlerts: context.activeAlerts,
          relatedWorkOrders: context.relatedWorkOrders.slice(0, 3)
        }
      };
    })
});
