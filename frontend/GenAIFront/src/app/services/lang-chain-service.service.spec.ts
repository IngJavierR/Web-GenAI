import { TestBed } from '@angular/core/testing';

import { LangChainServiceService } from './lang-chain-service.service';

describe('LangChainServiceService', () => {
  let service: LangChainServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LangChainServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
