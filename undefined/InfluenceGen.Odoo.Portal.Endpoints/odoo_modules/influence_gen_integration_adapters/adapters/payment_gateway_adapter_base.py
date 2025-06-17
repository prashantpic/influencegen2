# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import abc
from odoo import models, api
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..dtos.payment_dtos import (
        PaymentInitiationRequestDto,
        PaymentResultDto,
        BankAccountVerificationRequestDto,
        BankAccountVerificationResultDto,
    )


class PaymentGatewayAdapterBase(models.AbstractModel):
    """
    Abstract Base Class for Payment Gateway and Bank Account Verification adapters.

    This class defines the contract for interacting with different payment
    gateways. It ensures that various payment service integrations can be
    implemented and used interchangeably through a consistent interface.

    REQ-IL-012: Define common interface for payment gateway adapters.
    REQ-IOKYC-008: Support bank account verification process.
    """
    _name = 'influence_gen.payment.gateway.adapter.base'
    _description = 'InfluenceGen Payment Gateway Adapter Base'

    @abc.abstractmethod
    @api.model
    def initiate_payment(self, payment_request_dto: 'PaymentInitiationRequestDto') -> 'PaymentResultDto':
        """
        Abstract method to initiate a payment through an external payment gateway.

        Concrete implementations will handle API calls, authentication,
        payload construction, response parsing, and error handling specific
        to the chosen payment gateway.

        :param payment_request_dto: An instance of `PaymentInitiationRequestDto`
                                    containing details for the payment.
        :type payment_request_dto: PaymentInitiationRequestDto
        :return: An instance of `PaymentResultDto` indicating the outcome
                 of the payment initiation.
        :rtype: PaymentResultDto
        :raises NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement the initiate_payment method.")

    @abc.abstractmethod
    @api.model
    def verify_bank_account(self, bank_details_dto: 'BankAccountVerificationRequestDto') -> 'BankAccountVerificationResultDto':
        """
        Abstract method to verify bank account details using an external service.

        Concrete implementations will manage communication with the specific
        bank verification provider, including API calls, authentication,
        and result interpretation.

        :param bank_details_dto: An instance of `BankAccountVerificationRequestDto`
                                 containing the bank account details to verify.
        :type bank_details_dto: BankAccountVerificationRequestDto
        :return: An instance of `BankAccountVerificationResultDto` with the
                 verification status.
        :rtype: BankAccountVerificationResultDto
        :raises NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement the verify_bank_account method.")